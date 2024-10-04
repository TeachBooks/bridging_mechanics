import numpy as np
import matplotlib.pyplot as plt

class Element:
    """
    The Element class keeps track of each element in the model, including cross-section properties, 
    element orientation (for coordinate system transformations), and the nodes that make up each element. 
    With the help of the Node class, it also keeps track of which Degrees of Freedom (DOFs) belong to each element.

    This class is responsible for providing the element stiffness matrix in the global coordinate system 
    (for subsequent assembly) and postprocessing element-level fields. 

    This class describes an element combining extension and Euler-Bernoulli bending. A similar (or inherited) 
    class could also be implemented for different element types (e.g., shear beam, Timoshenko beam, cable elements, etc). 
    For simplicity, it is assumed that elements are all arranged in a 2D plane.

    Attributes:
        nodes (list): The two nodes of the element.
        EA (float): The axial stiffness of the element.
        EI (float): The flexural stiffness of the element.

    Methods:
        clear(): Clears the counting of elements.
        __init__(self, nodes): Initializes an Element object.
        set_section(self, props): Sets the section properties of the element.
        global_dofs(self): Returns the global degrees of freedom associated with the element.
        stiffness(self): Calculate the stiffness matrix of the element.
        add_distributed_load(self, q): Adds a distributed load to the element.
        bending_moments(self, u_global, num_points=2): Calculate the bending moments along the element.
        full_displacement(self, u_global, num_points=2): Calculates the displacement along the element.
        plot_moment_diagram(self, u_elem, num_points=10, global_c=False, scale=1.0): Plots the bending moment diagram of the element.
        plot_displaced(self, u_elem, num_points=10, global_c=False, scale=1.0): Plots the displaced element.
        __str__(self): Returns a string representation of the Element object.
    """

    ne = 0

    def clear():
        """
        Clears the counting of elements

        This method resets the class-level counters for number of elements. 
        It should be used when you want to start a new problem from scratch.
        """
        Element.ne = 0
        
    def __init__(self, node1, node2):
        """
        Initializes an Element object.

        Parameters:
        - node1 (Node): The first node of the element.
        - node2 (Node): The second node of the element.

        Attributes:
        - nodes (list): A list of Node objects representing the nodes of the element.
        - L (float): Length of the element.
        - cos (float): Cosine of the element's orientation angle.
        - sin (float): Sine of the element's orientation angle.
        - T (ndarray): Transformation matrix.
        - Tt (ndarray): Transpose of the transformation matrix.

        Returns:
        None
        """
        self.nodes = [node1, node2]

        self.L = np.sqrt((self.nodes[1].x - self.nodes[0].x)**2.0 + (self.nodes[1].z - self.nodes[0].z)**2.0)

        self.alpha = np.arctan2( - (self.nodes[1].z - self.nodes[0].z) , (self.nodes[1].x - self.nodes[0].x))

        T = np.zeros((6, 6))

        T[0, 0] = T[1, 1] = T[3, 3] = T[4, 4] = np.cos(self.alpha)
        T[0, 1] = T[3, 4] = -np.sin(self.alpha)
        T[1, 0] = T[4, 3] = np.sin(self.alpha)
        T[2, 2] = T[5, 5] = 1

        self.T = T
        self.Tt = np.transpose(T)

        self.q = np.array([0,0])
        self.local_element_load = np.array([0,0,0,0,0,0])
        
        Element.ne += 1

    def set_section(self, props):
        """
        Sets the section properties of the element.

        Parameters:
        - props (dict): A dictionary containing the section properties.
                        The dictionary should have the following keys:
                        - 'EA': The axial stiffness of the element.
                        - 'EI': The flexural stiffness of the element.

        Returns:
        None
        """
        if 'EA' in props:
            self.EA = props['EA']
        else:
            self.EA = 1.e20
        if 'EI' in props:
            self.EI = props['EI']
        else:
            self.EI = 1.e20

    def global_dofs(self):
        """
        Returns the global degrees of freedom associated with the element.

        Returns:
            numpy.ndarray: Array containing the global degrees of freedom.
        """
        return np.hstack((self.nodes[0].dofs, self.nodes[1].dofs))

    def stiffness(self):
        """
        Calculate the stiffness matrix of the element.

        Returns:
        np.ndarray: The stiffness matrix of the element.
        """
        k = np.zeros((6, 6))

        EA = self.EA
        EI = self.EI
        L = self.L

        # Extension contribution

        k[0, 0] = k[3, 3] = EA / L
        k[3, 0] = k[0, 3] = -EA / L

        # Bending contribution

        k[1, 1] = k[4, 4] = 12.0 * EI / L / L / L
        k[1, 4] = k[4, 1] = -12.0 * EI / L / L / L
        k[1, 2] = k[2, 1] = k[1, 5] = k[5, 1] = -6.0 * EI / L / L
        k[2, 4] = k[4, 2] = k[4, 5] = k[5, 4] = 6.0 * EI / L / L
        k[2, 2] = k[5, 5] = 4.0 * EI / L
        k[2, 5] = k[5, 2] = 2.0 * EI / L

        return np.matmul(np.matmul(self.Tt, k), self.T)

    def add_distributed_load(self, q):
        """
        Adds a distributed load to the element.

        Parameters:
            q (list): List of distributed load in local x and z direction.

        Returns:
            None
        """

        l = self.L
        self.q = np.array(q)

        self.local_element_load = [0.5 * q[0] * l, 0.5 * q[1] * l, -1.0 / 12.0 * q[1] * l * l, 0.5 * q[0] * l, 0.5 * q[1] * l, 1.0 / 12.0 * q[1] * l * l]

        global_element_load = np.matmul(self.Tt, np.array(self.local_element_load))

        self.nodes[0].add_load(global_element_load[0:3]) #YOUR CODE HERE
        self.nodes[1].add_load(global_element_load[3:6]) #YOUR CODE HERE

    def bending_moments(self, u_global, num_points=2):
        """
        Calculate the bending moments along the element.

        Parameters:
        - u_global (numpy.ndarray): Global displacement vector.
        - num_points (int): Number of points to evaluate the bending moments. Default is 2.

        Returns:
        - M (numpy.ndarray): Array of bending moments at the specified points.
        """

        l = self.L
        q = self.q[1]
        EI = self.EI

        local_x = np.linspace(0.0, l, num_points)

        local_disp = np.matmul(self.T, u_global)

        w_1 = local_disp[1]
        phi_1 = local_disp[2]
        w_2 = local_disp[4]
        phi_2 = local_disp[5]

        M = (-l ** 5.0 * q + 6.0 * l ** 4.0 * q * local_x
             - 6.0 * q * local_x * local_x * l ** 3.0 - 48.0 * (phi_1 + phi_2 / 2.0) * EI * l ** 2.0
             + 72.0 * EI * ((phi_1 + phi_2) * local_x + w_1 - w_2) * l - 144.0 * local_x * EI * (w_1 - w_2)) / 12.0 / l ** 3.0
        
        return M
    
    def full_displacement (self, u_global, num_points=2):
        """
        Calculates the displacement along the element.

        Args:
            u_global (numpy.ndarray): Global displacement vector of the element.
            num_points (int, optional): Number of points to calculate the bending moments. Default is 2.

        Returns:
            numpy.ndarray: Array of displacement along the element.
        """
        L = self.L
        q = self.q[1]
        q_x = self.q[0]
        EI= self.EI
        EA = self.EA

        x = np.linspace ( 0.0, L, num_points )

        ul = np.matmul ( self.T, u_global )

        u_1   = ul[0]
        w_1   = ul[1]
        phi_1 = ul[2]
        u_2   = ul[3]
        w_2   = ul[4]
        phi_2 = ul[5]

        u = q_x*(-L*x/(2*EA) + x**2/(2*EA)) + u_1*(1 - x/L) + u_2*x/L
        w = phi_1*(-x + 2*x**2/L - x**3/L**2) + phi_2*(x**2/L - x**3/L**2) + q*(L**2*x**2/(24*EI) - L*x**3/(12*EI) + x**4/(24*EI)) + w_1*(1 - 3*x**2/L**2 + 2*x**3/L**3) + w_2*(3*x**2/L**2 - 2*x**3/L**3)
        
        return u, w
    
    def plot_moment_diagram (self, u_elem, num_points=10, global_c=False, scale=1.0):
        """
        Plots the bending moment diagram of the element.

        Args:
            u_global (numpy.ndarray): Global displacement vector of the element.
            num_points (int, optional): Number of points to calculate the bending moments. Default is 2.
            global_c (bool, optional): If True, plots the bending moment diagram in the global coordinate system. Default is False (plots in local coordinate system).
            scale (float, optional): Scale factor for the bending moment diagram. Default is 1.0.

        Returns:
            None
        """
        import matplotlib.pyplot as plt

        x = np.linspace ( 0.0, self.L, num_points )
        M = self.bending_moments ( u_elem, num_points )
        xM_local = np.vstack((np.hstack([0,x,x[-1]]),np.hstack([0,M,0])*scale))
        if global_c:
            xM_global = np.matmul(self.Tt[0:2,:2],xM_local)
            xz_start_node = np.vstack((np.ones(num_points+2)*self.nodes[0].x, np.ones(num_points+2)*self.nodes[0].z))
            xz_Mlijn = xM_global + xz_start_node
            p = plt.plot(xz_Mlijn[0,:],xz_Mlijn[1,:])
            X0= self.nodes[0].x
            Z0= self.nodes[0].z
            X1= self.nodes[1].x
            Z1= self.nodes[1].z
            plt.plot((X0, X1), (Z0, Z1), color=p[0].get_color())
            plt.axis('off')
            plt.axis('equal')
        else:
            p = plt.plot(xM_local[0,:],xM_local[1,:])
            plt.xlabel ( "x" )
            plt.ylabel ( "M" )
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.title('Moment line')

    def plot_displaced(self, u_elem, num_points=10, global_c=False, scale=1.0):
        """
        Plots the displacd element.

        Args:
            u_global (numpy.ndarray): Global displacement vector of the element.
            num_points (int, optional): Number of points to calculate the bending moments. Default is 2.
            global_c (bool, optional): If True, plots the displacement diagram in the global coordinate system. Default is False (plots in local coordinate system).
            scale (float, optional): Scale factor for the displacement diagram. Default is 1.0.

        Returns:
            None
        """

        x = np.linspace ( 0.0, self.L, num_points )
        u, w = self.full_displacement ( u_elem, num_points )
        uw_local = np.vstack((x+u*scale,w*scale))
        if global_c:
            uw_global = np.matmul(self.Tt[:2,:2],uw_local)
            xz_start_node = np.vstack((np.ones(num_points)*self.nodes[0].x, np.ones(num_points)*self.nodes[0].z))
            uw = uw_global + xz_start_node
            p =  plt.plot(uw[0,:],uw[1,:])
            X0= self.nodes[0].x
            Z0= self.nodes[0].z
            X1= self.nodes[1].x
            Z1= self.nodes[1].z
            plt.plot((X0, X1), (Z0, Z1), color=p[0].get_color(),alpha=0.3)
            plt.axis('off')
            plt.axis('equal')
        else:
            p = plt.plot(uw_local[0,:],uw_local[1,:])
            plt.plot((0, self.L), (0, 0), color=p[0].get_color(),alpha=0.3)
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.title('Displaced structure')
    
    def plot_numbered_structure(self,beam_number):
        """
        Plots the nodes of the structure with their node numbers.

        Returns:
            None
        """

        X0= self.nodes[0].x
        Z0= self.nodes[0].z
        X1= self.nodes[1].x
        Z1= self.nodes[1].z
        node_num = []
        node_num.append(self.nodes[0].dofs[0] // 3)
        node_num.append(self.nodes[1].dofs[0] // 3)
        plt.plot((X0, X1), (Z0, Z1), color='black',alpha=0.3)
        for i, node in enumerate(self.nodes):
            plt.text(node.x, node.z, f'[{node.dofs[0] // 3}]', fontsize=12, ha='center', va='center')
        plt.text((X0+X1)/2, (Z0+Z1)/2, f'({beam_number})', fontsize=12, ha='center', va='center')
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.axis('off')
        plt.axis('equal')

    def plot_numbered_structure(self,beam_number):
        """
        Plots the nodes and elements of the structure with their node and element numbers.

        Returns:
            None
        """

        X0= self.nodes[0].x
        Z0= self.nodes[0].z
        X1= self.nodes[1].x
        Z1= self.nodes[1].z
        node_num = []
        node_num.append(self.nodes[0].dofs[0] // 3)
        node_num.append(self.nodes[1].dofs[0] // 3)
        plt.plot((X0, X1), (Z0, Z1), color='black',alpha=0.3)
        for i, node in enumerate(self.nodes):
            plt.text(node.x, node.z, f'[{node.dofs[0] // 3}]', fontsize=12, ha='center', va='center')
        plt.text((X0+X1)/2, (Z0+Z1)/2, f'({beam_number})', fontsize=12, ha='center', va='center')
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.axis('off')
        plt.axis('equal')


    def __str__(self):
        """
        Returns a string representation of the Element object.
        
        The string includes the values of the node1, node2 attributes.
        """
        return f"Element connecting:\nnode #1:\n {self.nodes[0]}\nwith node #2:\n {self.nodes[1]}"
    

class TimoshenkoElement (Element):
    """
    TimoshenkoElement class represents a Timoshenko element in a structural analysis loaded with a sinusodial load.

    Attributes:
        node1 (Node): The first node of the element.
        node2 (Node): The second node of the element.
        EA (float): Axial stiffness of the element.
        EI (float): Bending stiffness of the element.
        GA (float): Shear stiffness of the element.
        L (float): Length of the element.

    Methods:
        set_section(props): Sets the section properties of the element.
        stiffness(): Calculates the stiffness matrix of the element.
        add_distributed_load(q): Adds a sinusodial load to the element.
        bending_moments(u_global, num_points=2): Calculates the bending moments along the element.

    Inherits from:
        Element: Base class for all structural elements.
    """
    def set_section(self,props):
        """
        Adds the shear stiffness to the section properties

        For details on the initial work, see:
        help(super().set_section)
        """
        super().set_section(props)
        self.GA = props['GA']
        
    def stiffness (self):
        """
        Calculate the stiffness matrix of the element.

        Does the same as the base class, but includes shear stiffness.
        """
        k = np.zeros ((6, 6))

        EA = self.EA
        EI = self.EI
        GA = self.GA
        L = self.L
        
        beta = 12.0*EI/GA/L/L

        # Extension contribution

        k[0,0] = k[3,3] = EA/L
        k[3,0] = k[0,3] = -EA/L

        # Bending/shear contribution

        k[1,1] = k[4,4] =  12.0 * EI / L / L / L / (beta+1.)
        k[1,4] = k[4,1] = -12.0 * EI / L / L / L / (beta+1.)
        k[1,2] = k[2,1] = k[1,5] = k[5,1] = -6.0 * EI / L / L / (beta+1.)
        k[2,4] = k[4,2] = k[4,5] = k[5,4] = 6.0 * EI / L / L / (beta+1.)
        k[2,2] = k[5,5] = (4.0+beta) * EI / L / (beta+1.)
        k[2,5] = k[5,2] = (2.0-beta) * EI / L / (beta+1.)

        return np.matmul ( np.matmul ( self.Tt, k ), self.T )
    
    def add_distributed_load (self,q):
        """
        Adds a sinusodial load to the element.

        Parameters:
            q (float): sinusodial load in local z direction.

        Returns:
            None
        """
        
        l = self.L
        pi = np.pi

        self.q = np.array([0,q])

        self.local_element_load = [ 0, 
              self.q[1]*l/pi, 
              -2.0*l*l*self.q[1]/pi/pi/pi, 
              0, 
              self.q[1]*l/pi, 
              2.0*l*l*self.q[1]/pi/pi/pi 
             ]

        eg = np.matmul ( self.Tt, np.array ( self.local_element_load ) )

        self.nodes[0].add_load ( eg[0:3] )
        self.nodes[1].add_load ( eg[3:6] )
        
    def bending_moments (self, u_global, num_points=2):
        """
        Calculates the bending moments along the element.

        Args:
            u_global (numpy.ndarray): Global displacement vector of the element.
            num_points (int, optional): Number of points to calculate the bending moments. Default is 2.

        Returns:
            numpy.ndarray: Array of bending moments along the element.
        """
        l = self.L
        q = self.q
        EI= self.EI
        pi = np.pi
        
        beta = 12.0*EI/self.GA/l/l

        x = np.linspace ( 0.0, l, num_points )
        M  = np.zeros(num_points)

        ul = np.matmul ( self.T, u_global )
        
        w1   = ul[1]
        phi1 = ul[2]
        w2   = ul[4]
        phi2 = ul[5]

        num = l**5*pi*q[1]*(beta+1)*np.sin(pi*x/l) + (((phi2-phi1)*beta-2*phi2-4*phi1)*l**2 + ((6*phi2+6*phi1)*x + 6*w1 - 6*w2)*l - 12*x*(w1-w2)) * EI*pi**3 -2*l**5*q[1]*(beta+1)
        den = l**3 * pi**3 * (beta+1)
        
        M = num/den
        
        return M
    
    def full_displacement (self, u_global, num_points=2):
        """
        Calculates the displacement along the element.

        Args:
            u_global (numpy.ndarray): Global displacement vector of the element.
            num_points (int, optional): Number of points to calculate the bending moments. Default is 2.

        Returns:
            numpy.ndarray: Array of displacement along the element.
        """
        L = self.L
        q = self.q[1]
        q_x = self.q[0]
        EI= self.EI
        pi = np.pi
        EA = self.EA
        beta = 12.0*EI/self.GA/L/L

        x = np.linspace ( 0.0, L, num_points )

        ul = np.matmul ( self.T, u_global )
        
        u_1   = ul[0]
        w_1   = ul[1]
        phi_1 = ul[2]
        u_2   = ul[3]
        w_2   = ul[4]
        phi_2 = ul[5]

        u = q_x*(-L*x/(2*EA) + x**2/(2*EA)) + u_1*(1 - x/L) + u_2*x/L
        w = x*((L*beta*phi_1 + L*beta*phi_2 - 2*beta*w_1 + 2*beta*w_2)/(2*L*beta + 2*L) - (pi**3*EI*L**2*beta*phi_1 + L**5*beta*q)/(pi**3*EI*L**2*beta)) + (-pi**3*EI*L*beta**2*phi_1 + pi**3*EI*L*beta**2*phi_2 - 4*pi**3*EI*L*beta*phi_1 - 2*pi**3*EI*L*beta*phi_2 + 6*pi**3*EI*beta*w_1 - 6*pi**3*EI*beta*w_2 - 2*L**4*beta**2*q - 2*L**4*beta*q)/(12*pi**3*EI*beta + 12*pi**3*EI) - 2*x**3*(L*beta*phi_1 + L*beta*phi_2 - 2*beta*w_1 + 2*beta*w_2)/(L**2*beta*(2*L*beta + 2*L)) - 6*x**2*(-pi**3*EI*L*beta**2*phi_1 + pi**3*EI*L*beta**2*phi_2 - 4*pi**3*EI*L*beta*phi_1 - 2*pi**3*EI*L*beta*phi_2 + 6*pi**3*EI*beta*w_1 - 6*pi**3*EI*beta*w_2 - 2*L**4*beta**2*q - 2*L**4*beta*q)/(L**2*beta*(12*pi**3*EI*beta + 12*pi**3*EI)) - 12*(-pi**3*EI*L**3*beta**3*phi_1 + pi**3*EI*L**3*beta**3*phi_2 - 4*pi**3*EI*L**3*beta**2*phi_1 - 2*pi**3*EI*L**3*beta**2*phi_2 - 6*pi**3*EI*L**2*beta**2*w_1 - 6*pi**3*EI*L**2*beta**2*w_2 - 12*pi**3*EI*L**2*beta*w_1 - 2*L**6*beta**3*q - 2*L**6*beta**2*q)/(L**2*beta*(144*pi**3*EI*beta + 144*pi**3*EI)) + L**4*q*(pi**2*beta + 12)*np.sin(pi*x/L)/(12*pi**4*EI)
        return u, w
