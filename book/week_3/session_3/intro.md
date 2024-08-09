(lesson3.3)=
# Lesson Friday September 20th

During today's lesson it's demonstrated how you to use the force method for statically indeterminate problems which only involve extension

## Demonstration
Given a structure as shown below:

```{figure} ./intro_data/structure.svg
:align: center

Structure
```

We can find the normal force distribution using the force method. Therefore, we need to know the degree of statically determinacy. The free-body-diagram of the full structure is as follows:

```{figure} ./intro_data/FBD.svg
:align: center

Free-body-diagram full structure
```

There are 4 unknown support reactions. With only 3 equilibrium equations this gives a first-order statically determinant structure.

To apply the force method we need to replace a part of the structure by a statically indeterminate force, which turns the structure into a statically determinate structure. To solve the statically indeterminate structure we need to include a compatibility condition.

## Define statically determinate structure with compatibility condition
In this structure, we choose to replace the right support with a rolling hinged support. This leads to a horizontal statically indeterminate force $B_\text{v}$ with the compatibility conditions $u_{h,\text{B}} = 0$:

```{figure} ./intro_data/SD.svg
:align: center

Statically determinate structure with compatibility condition
```

## Solve displacements statically determinate structure in terms of statically indeterminate force
The force distribution and displacements in this statically determinate structure is now solved for in terms of $B_\text{h}$.

First, the

```{figure} ./intro_data/FBD.svg
:align: center

Free-body-diagram full structure
```

$$
\begin{array}{l}
\sum {{{\left. T \right|}_{\rm{A}}} = 0}  \to {B_{\rm{v}}} = 5{\text{ kN}}\\
\sum {{F_{\rm{v}}} = 0}  \to {A_{\rm{v}}} = 5{\text{ kN}}\\
\sum {{F_{\rm{h}}} = 0}  \to {A_{\rm{h}}} = {B_{\rm{h}}}
\end{array}
$$

Leading to:

```{figure} ./intro_data/FBD_sol.svg
:align: center

Free-body-diagram full structure
```