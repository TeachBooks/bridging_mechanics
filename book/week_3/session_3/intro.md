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

### Support reactions
First, the support reactions are solved for

```{figure} ./intro_data/FBD.svg
:align: center

Free-body-diagram full structure
```

$$
\begin{array}{c}
\sum {{{\left. T \right|}_{\rm{A}}} = 0}  \to {B_{\rm{v}}} = 5{\text{ kN}}\\
\sum {{F_{\rm{v}}} = 0}  \to {A_{\rm{v}}} = 5{\text{ kN}}\\
\sum {{F_{\rm{h}}} = 0}  \to {A_{\rm{h}}} = {B_{\rm{h}}}
\end{array}
$$

Leading to:

```{figure} ./intro_data/FBD_sol.svg
:align: center

Free-body-diagram full structure with resulting support reactions
```

### Section forces

The section forces are solved for, starting with the forces in $\text{BE}$ and $\text{BD}$:

```{figure} ./intro_data/FBD_B.svg
:align: center

Free-body-diagram joint $\text{B}$
```

$$
\begin{array}{c}
\sum {{F_{\rm{v}}} = 0}  \to {N_{{\rm{BE}}}} = -6.25{\text{ kN}}\\
\sum {{F_{\rm{h}}} = 0}  \to {N_{{\rm{BD}}}} =  3.75 - {B_{\rm{h}}}
\end{array}
$$

```{figure} ./intro_data/FBD_B_sol.svg
:align: center

Free-body-diagram joint $\text{B}$ with resulting sections forces
```

Now, let's continue with a section through beams $\text{AB}$, $\text{CD}$ and $\text{CE}$:

```{figure} ./intro_data/FBD_AC.svg
:align: center

Free-body-diagram part $\text{AC}$
```

$$
\begin{array}{c}
\sum {{F_{\rm{v}}} = 0}  \to {N_{{\rm{CD}}}} =  - 6.25{\rm{ kN}}\\
{\sum {\left. T \right|} _{\rm{D}}} = 0 \to {N_{CE}} =  - 7.5{\rm{ kN}}\\
\sum {{F_{\rm{h}}} = 0}  \to {N_{{\rm{BD}}}} = 11.25 - {B_{\rm{h}}}
\end{array}
$$

```{figure} ./intro_data/FBD_AC_sol.svg
:align: center

Free-body-diagram part $\text{AC}$ with resulting section forces
```

Thirdly, let's continue with the joint $\text{D}$:

```{figure} ./intro_data/FBD_D.svg
:align: center

Free-body-diagram joint $\text{D}$
```

$$\sum {{F_{\rm{v}}} = 0}  \to {N_{{\rm{DE}}}} =  - 6.25{\text{ kN}}$$

```{figure} ./intro_data/FBD_D_sol.svg
:align: center

Free-body-diagram joint $\text{D}$
```

And finally joint $\text{C}$:

```{figure} ./intro_data/FBD_C.svg
:align: center

Free-body-diagram joint $\text{D}$
```

$$\sum {{F_{\rm{v}}} = 0}  \to {N_{{\rm{DE}}}} =  - 18.75{\text{ kN}}$$

```{figure} ./intro_data/FBD_C_sol.svg
:align: center

Free-body-diagram joint $\text{D}$
```

### Shortening/lengthening of elements

Now, for each element the shortening / lengthening can be calculated:

