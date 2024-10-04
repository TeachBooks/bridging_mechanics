import numpy as np
import matplotlib.pyplot as plt

class Node:
    """
    The Node class is used to store node information and keep track of the total number of 
    Degrees of Freedom (DOFs) of the problem. It introduces automatic bookkeeping in its 
    initialization, which efficiently keeps track of which DOFs belong to which nodes. This 
    makes it easier to assemble matrices from multiple elements.

    Attributes:
        x (float): The x-coordinate of the node.
        z (float): The z-coordinate of the node.
        p (numpy.array):  The load vector of the node.
        dofs (list): The Degrees of Freedom associated with the node.

    Methods:
        clear(): Clears the counting of degrees of freedom and number of nodes.
        __init__(x, z): The constructor for Node class.
        add_load(p): Adds the given loads to the node.
        get_coords(): Returns the coordinates of the node.
        __str__(): Returns a string representation of the node.
    """
    ndof = 0
    nn   = 0
    
    def clear():
        """
        Clears the counting of degrees of freedom and number of nodes.

        This method resets the class-level counters for degrees of freedom and number of nodes. 
        It should be used when you want to start a new problem from scratch.
        """
        Node.ndof = 0
        Node.nn = 0
        
    def __init__ (self, x, z): 
        """
        The constructor for Node class.

        Parameters:
            x (float):        The x-coordinate of the node.
            z (float):        The z-coordinate of the node.
            p (numpy.array):  The load vector of the node.
            dofs (list):      The Degrees of Freedom (u (in direction of x), w (in direction of z), phi (from z to x)) associated with the node.
        """

        self.x     = x
        self.z     = z
        self.p     = np.zeros(3)
        self.nodal_load = np.zeros(3)

        self.dofs  = [Node.ndof, Node.ndof+1, Node.ndof+2]

        Node.ndof += 3
        Node.nn   += 1

    def add_load (self, p, nodal_load = False):
        """
        Adds the given loads to the node.

        The load is a vector p, which includes the load in the x and y direction and a moment. 
        These loads are added to the existing loads of the node.

        Parameters:
            p (numpy.array): A vector containing the load in the x direction, the load in the y direction, 
                             and the moment. 
        """
        self.p += p
        if nodal_load == True:
            self.nodal_load += p

    def get_coords(self):
        """
        Returns the coordinates of the node.

        Returns:
           numpy.array: An array containing the x and z coordinates of the node.
        """
        return np.array([self.x, self.z])
    
    def plot_FBD(self, elems, nodes, con, u_full, support_reactions):
        """
        Plots the free body diagram of the node.

        This method plots the free body diagram of the node, showing the applied loads and the 
        reaction forces. 

        Parameters:
            elems (list): A list of elements in the structure.
            con (Constrainer): The constrainer object.
            u_full (numpy.array): A vector containing the displacements of all degrees of freedom.
            support_reactions (list): A list containing the support reactions.
        """
        dofs_node_2 = self.dofs
        elems_node_2 = []
        # Find the elements that contain the node and store the elements, an index indicating whether the relevant edge is the first or second node, the angle of the element and the edge forces.
        for elem in elems:
            if set(dofs_node_2).issubset(set(elem.global_dofs())):
                edge_forces = (elem.T @ elem.stiffness() @ u_full[elem.global_dofs()]) - elem.local_element_load
                if list(elem.global_dofs()).index(dofs_node_2[0]) == 0:
                    subset_index = [0,1,2]
                    alpha_node = elem.alpha
                    edge_forces = [-edge_forces[0],-edge_forces[1],-edge_forces[2]] #define in local coordinates
                else:
                    subset_index = [3,4,5]
                    alpha_node = elem.alpha + np.pi
                    edge_forces = [edge_forces[3],edge_forces[4],-edge_forces[5]] #define in local coordinates
                elems_node_2.append([elem, subset_index, alpha_node,edge_forces])
        
        # Find the nodal forces acting on the node from support reactions and nodal loads and store the forces and the direction of the forces (in terms of dof).
        nodal_forces_node_2 = []
        for dof in dofs_node_2:
            if dof in con.cons_dofs:
                temp = []
                temp.append(support_reactions[con.cons_dofs.index(dof)])
                temp.append(dof - (dof // 3) * 3)
                nodal_forces_node_2.append(temp)
        for dof in dofs_node_2:
            temp = []
            temp.append(self.nodal_load[dof - (dof // 3) * 3])
            temp.append(dof - (dof // 3) * 3)
            nodal_forces_node_2.append(temp)
        
        # Find the maximum value of the forces and moments acting on the node.
        max_value = 0
        max_moment = 0
        for elem in elems_node_2:
            max_value = max(max_value, abs(elem[3][0]), abs(elem[3][1]))
        for nodal_force in nodal_forces_node_2:
            if nodal_force[1] <= 1:
                max_value = max(max_value,abs(nodal_force[0]))
            elif nodal_force[1] == 2:
                max_moment = max(max_moment,abs(nodal_force[0]))
        for elem in elems_node_2:
            max_moment = max(max_moment, abs(elem[3][2]))

        # Plot the free body diagram
        fig, ax = plt.subplots(figsize=(6,6))
        for elem in elems_node_2:
            r = 1 # length of the elements to be shown.
            theta = elem[2]
            length1 = elem[3][0]
            length2 = elem[3][1]
            
            # Normalize the lengths
            max_length = max_value
            length1_normalized = np.sign(length1)/4 + 0.5*length1 / max_length
            length2_normalized = np.sign(length2)/4 + 0.5*length2 / max_length
            length3_normalized = abs(np.sign(elem[3][2])*0.1 + 0.2*elem[3][2] / max_moment)
            
            # Convert polar coordinates to Cartesian coordinates
            x1 = r * np.cos(theta)
            y1 = r * np.sin(theta)
            
            # Create a plot

            # plot part of the beam
            ax.plot([x1, 0], [y1, 0], color='black')
            ax.plot(0,0,color='black',marker='o')

            # Plot the normal forces
            if length1 < 0.0001 and length1 > -0.0001:
                pass
            elif length1_normalized > 0:
                ax.annotate(text='', xytext=(x1,y1), xy=(x1 + length1_normalized*np.cos(theta),y1 + length1_normalized*np.sin(theta)), arrowprops=dict(arrowstyle='simple'),annotation_clip=False)
                ax.text(x1 + length1_normalized*np.cos(theta),y1 + length1_normalized*np.sin(theta), f'{abs(length1):.2f}',  ha='left', va='bottom')
            else:
                ax.annotate(text='', xy=(x1,y1), xytext=(x1 - length1_normalized*np.cos(theta),y1 - length1_normalized*np.sin(theta)), arrowprops=dict(arrowstyle='simple'),annotation_clip=False)
                ax.text(x1 - length1_normalized*np.cos(theta),y1 - length1_normalized*np.sin(theta), f'{abs(length1):.2f}', ha='left', va='bottom')

            # plot the shear forces
            if length2 < 0.0001 and length2 > -0.0001:
                pass
            else:
                ax.annotate(text='', xytext=(x1,y1), xy=(x1 + length2_normalized*np.cos(theta - np.pi /2),y1 + length2_normalized*np.sin(theta - np.pi / 2)), arrowprops=dict(arrowstyle='simple'),annotation_clip=False)
                ax.text(x1 + length2_normalized*np.cos(theta - np.pi / 2),y1 + length2_normalized*np.sin(theta - np.pi / 2), f'{abs(length2):.2f}',  ha='left', va='bottom')
            
            # plot the moments
            if elem[3][2]<0.0001 and elem[3][2]>-0.0001:
                pass
            elif elem[3][2]>0:
                ax.annotate(text='', xy=(x1 + length3_normalized*np.cos(theta+np.pi/2),y1 + length3_normalized*np.sin(theta + np.pi / 2)), xytext=(x1 - length3_normalized*np.cos(theta+np.pi/2),y1 - length3_normalized*np.sin(theta + np.pi / 2 )), arrowprops=dict(arrowstyle='simple',connectionstyle="arc3,rad=0.785"),annotation_clip=False)
                ax.text(x1 + length3_normalized*np.cos(theta + np.pi / 4),y1 + length3_normalized*np.sin(theta + np.pi / 4), f'{abs(elem[3][2]):.2f}',  ha='left', va='center')
            elif elem[3][2]<0:
                ax.annotate(text='', xy=(x1 - length3_normalized*np.cos(theta+np.pi/2),y1 - length3_normalized*np.sin(theta + np.pi / 2)), xytext=(x1 + length3_normalized*np.cos(theta+np.pi/2),y1 + length3_normalized*np.sin(theta + np.pi / 2 )), arrowprops=dict(arrowstyle='simple',connectionstyle="arc3,rad=-0.785"),annotation_clip=False)
                ax.text(x1 + length3_normalized*np.cos(theta - np.pi / 4),y1 + length3_normalized*np.sin(theta - np.pi / 4), f'{abs(elem[3][2]):.2f}',  ha='left', va='center')
        
        # plot the nodal forces
        for nodal_force in nodal_forces_node_2:
            length_normalized = np.sign(nodal_force[0])/4 + 0.5*nodal_force[0] / max_length
            if nodal_force[1] == 0:
                theta = 0
            elif nodal_force[1] == 1:
                theta = -90/180*np.pi
            elif nodal_force[1] == 2:
                theta = 0
            if nodal_force[0] < 0.0001 and nodal_force[0] > -0.0001:
                pass
            elif nodal_force[1] <= 1:
                length_normalized = np.sign(nodal_force[0])/4 + 0.5* nodal_force[0] / max_value
                ax.annotate(text='', xytext=(0,0), xy=(length_normalized*np.cos(theta),+length_normalized*np.sin(theta)), arrowprops=dict(arrowstyle='simple'),annotation_clip=False)
                ax.text(length_normalized*np.cos(theta),length_normalized*np.sin(theta), f'{abs(nodal_force[0]):.2f}', ha = 'left', va = 'bottom')
            elif nodal_force[1] == 2:
                length_normalized = np.sign(nodal_force[0])*0.1 + 0.2* nodal_force[0] / max_moment
                ax.annotate(text='', xy=(-length_normalized*np.cos(theta+np.pi/2),-length_normalized*np.sin(theta + np.pi / 2)), xytext=(length_normalized*np.cos(theta+np.pi/2), length_normalized*np.sin(theta + np.pi / 2 )), arrowprops=dict(arrowstyle='simple',connectionstyle="arc3,rad=0.785"),annotation_clip=False)
                ax.text(-length_normalized*np.cos(theta + np.pi / 4),-length_normalized*np.sin(theta + np.pi / 4), f'{abs(nodal_force[0]):.2f}',  ha='left', va='center')


        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_xlim([-1,1])
        ax.set_ylim([-1,1])
        plt.title('Free body diagram of node at x = '+str(self.x)+' and z = '+str(self.z)+'\n\n\n\n\n\n\n\n\n\n')
        plt.tight_layout()

    def __str__(self):
        """
        Returns a string representation of the node.

        Returns:
            str: A string representation of the node.
        """
        return f"This node has:\n - x coordinate={self.x},\n - z coordinate={self.z},\n - degrees of freedom={self.dofs},\n - load vector={self.p})"