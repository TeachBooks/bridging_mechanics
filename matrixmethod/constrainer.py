import numpy as np
import matplotlib.pyplot as plt

class Constrainer:
    """
    A class that represents a constrainer for fixing degrees of freedom in a structural analysis.

    Attributes:
        cons_dofs (list): A list of constrained degrees of freedom.
        cons_vals (list): A list of corresponding constraint values.

    Methods:
        fix_dof: Fixes a degree of freedom at a specific value.
        fix_node: Fixes all degrees of freedom of a node.
        full_disp: Combines the displacements of free and constrained degrees of freedom.
        constrain: Applies the constraints to the stiffness matrix and load vector.
        support_reactions: Calculates the support reactions based on the constrained displacements.
    """

    def __init__(self):
        """
        Initializes a new instance of the Constrainer class.

        Attributes:
            cons_dofs (list): A list of constrained degrees of freedom.
            cons_vals (list): A list of corresponding constraint values.  
        """
        self.cons_dofs = []
        self.cons_vals = []

    def fix_dof (self, node, dof, value = 0):
        """
        Fixes a degree of freedom at a specific value.

        Args:
            node (Node): The node object.
            dof (int): The index of the degree of freedom to fix.
            value (float, optional): The value to fix the degree of freedom at. Defaults to 0.
        """
        self.cons_dofs.append(node.dofs[dof])
        self.cons_vals.append(value)
 
    def fix_node (self, node):
        """
        Fixes all degrees of freedom of a node.

        Args:
            node (Node): The node object.
        """
        for dof in [0,1,2]:
            self.fix_dof (node, dof)    

    def full_disp (self,u_free):
        """
        Combines the displacements of free and constrained degrees of freedom.

        Args:
            u_free (numpy.ndarray): The displacements of the free degrees of freedom.

        Returns:
            numpy.ndarray: The combined displacements of all degrees of freedom.
        """
        u_full = np.zeros(len(self.free_dofs) + len(self.cons_dofs))
        
        u_full[self.free_dofs] = u_free
        u_full[self.cons_dofs] = self.cons_vals
        
        return u_full
    
    def constrain (self, k, f):
        """
        Applies the constraints to the stiffness matrix and load vector.

        Args:
            k (numpy.ndarray): The stiffness matrix.
            f (numpy.ndarray): The load vector.

        Returns:
            tuple: A tuple containing the stiffness matrix corresponding to free dofs and the corresponding load vector.
        """
        self.free_dofs = [i for i in range(len(f)) if i not in self.cons_dofs]
        
        Kff = k[np.ix_(self.free_dofs,self.free_dofs)]
        Kfc = k[np.ix_(self.free_dofs,self.cons_dofs)]
        Ff = f[self.free_dofs]

        return Kff, Ff - np.matmul(Kfc,self.cons_vals)

    def support_reactions (self,k,u_free,f):       
        """
        Calculates the support reactions based on the constrained displacements.

        Args:
            k (numpy.ndarray): The stiffness matrix.
            u_free (numpy.ndarray): The displacements of the free degrees of freedom.
            f (numpy.ndarray): The load vector.

        Returns:
            numpy.ndarray: The support reactions.
        """
        Kcf = k[np.ix_(self.cons_dofs,self.free_dofs)]
        Kcc = k[np.ix_(self.cons_dofs,self.cons_dofs)]
        
        return np.matmul(Kcf,u_free) + np.matmul(Kcc,self.cons_vals) - f[self.cons_dofs]
    
    def plot_free_body_diagram(self,nodes,elems,support_reactions,scale=1):
        """
        Plots the free body diagram of the structure.

        Args:
            nodes (list): A list of nodes in the structure.
            elems (list): A list of elements in the structure.
            support_reactions (numpy.ndarray): The support reactions.
        """
        # Extract the support reactions and store the values, the direction in terms of degree of freedom, and the location of the node x and z coordinates
        nodal_forces_node_2 = []
        for dof in self.cons_dofs:
            temp = []
            temp.append(support_reactions[self.cons_dofs.index(dof)])
            temp.append(dof - (dof // 3) * 3)
            for node in nodes:
                if dof in node.dofs:
                    temp.append(node.x)
                    temp.append(node.z)
            nodal_forces_node_2.append(temp)
        
        # Find the maximum value of the forces and moments
        max_value = 0
        max_moment = 0
        for nodal_force in nodal_forces_node_2:
            if nodal_force[1] <= 1:
                max_value = max(max_value,abs(nodal_force[0]))
            elif nodal_force[1] == 2:
                max_moment = max(max_moment,abs(nodal_force[0]))

        # scale the forces and moments
        max_value = max_value / scale
        max_moment = max_moment / scale

        # plot the structure itselfs
        fig, ax = plt.subplots(figsize=(6,6))
        for elem in elems:
            X0= elem.nodes[0].x
            Z0= elem.nodes[0].z
            X1= elem.nodes[1].x
            Z1= elem.nodes[1].z
            plt.plot((X0, X1), (Z0, Z1), color='black',alpha=0.3)
            plt.axis('off')
            plt.axis('equal')
            if not plt.gca().yaxis_inverted():
                plt.gca().invert_yaxis()

        # plot the support reactions
        for nodal_force in nodal_forces_node_2:    
            if nodal_force[1] == 0:
                theta = 0
            elif nodal_force[1] == 1:
                theta = 90/180*np.pi
            elif nodal_force[1] == 2:
                theta = 0
            if nodal_force[0] < 0.0001 and nodal_force[0] > -0.0001:
                pass
            elif nodal_force[1] <= 1:
                length_normalized = np.sign(nodal_force[0])/4 + 0.5* nodal_force[0] / max_value
                ax.annotate(text='', xytext=(nodal_force[2],nodal_force[3]), xy=(nodal_force[2]+length_normalized*np.cos(theta),nodal_force[3]+length_normalized*np.sin(theta)), arrowprops=dict(arrowstyle='simple'),annotation_clip=False)
                ax.text(nodal_force[2]+length_normalized*np.cos(theta),nodal_force[3]+length_normalized*np.sin(theta), f'{abs(nodal_force[0]):.2f}', ha = 'left', va = 'bottom')
            elif nodal_force[1] == 2:
                length_normalized = np.sign(nodal_force[0])*0.1 + 0.2* nodal_force[0] / max_moment
                ax.annotate(text='', xy=(nodal_force[2] + length_normalized*np.cos(theta+np.pi/2),nodal_force[3] + length_normalized*np.sin(theta + np.pi / 2)), xytext=(nodal_force[2] - length_normalized*np.cos(theta+np.pi/2),nodal_force[3] - length_normalized*np.sin(theta + np.pi / 2 )), arrowprops=dict(arrowstyle='simple',connectionstyle="arc3,rad=0.785"),annotation_clip=False)
                ax.text(nodal_force[2] - length_normalized*np.cos(theta + np.pi / 4),nodal_force[3] + length_normalized*np.sin(theta + np.pi / 4), f'{abs(nodal_force[0]):.2f}',  ha='left', va='center')

        ax.set_aspect('equal')
        ax.axis('off')
        plt.title('Free body diagram without external forces\n\n')
        plt.tight_layout()



    def __str__(self):
        """
        Returns a string representation of the Constrainer object.

        Returns:
            str: A string representation of the Constrainer object.
        """
        return f"This constrainer has constrained the degrees of freedom: {self.cons_dofs} with corresponding constrained values: {self.cons_vals})"