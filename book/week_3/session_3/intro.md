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

There are 4 unknown support reactions. With only 3 equilibrium equations for this self-contained structure, it can be concluded that this structure is a first-order statically determinant structure.

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
\sum {{F_{\rm{v}}} = 0}  \to {A_{\rm{v}}} = 15{\text{ kN}}\\
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

Now, let's continue with a section through beams $\text{AD}$, $\text{CD}$ and $\text{CE}$:

```{figure} ./intro_data/FBD_AC.svg
:align: center

Free-body-diagram part $\text{AC}$
```

$$
\begin{array}{c}
\sum {{F_{\rm{v}}} = 0}  \to {N_{{\rm{CD}}}} =  - 6.25{\rm{ kN}}\\
{\sum {\left. T \right|} _{\rm{D}}} = 0 \to {N_{CE}} =  - 7.5{\rm{ kN}}\\
\sum {{F_{\rm{h}}} = 0}  \to {N_{{\rm{AD}}}} = 11.25 - {B_{\rm{h}}}
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

$$\sum {{F_{\rm{v}}} = 0}  \to {N_{{\rm{DE}}}} =  6.25{\text{ kN}}$$

```{figure} ./intro_data/FBD_D_sol.svg
:align: center

Free-body-diagram joint $\text{D}$
```

And finally joint $\text{C}$:

```{figure} ./intro_data/FBD_C.svg
:align: center

Free-body-diagram joint $\text{D}$
```

$$\sum {{F_{\rm{v}}} = 0}  \to {N_{{\rm{AC}}}} =  - 18.75{\text{ kN}}$$

```{figure} ./intro_data/FBD_C_sol.svg
:align: center

Free-body-diagram joint $\text{D}$
```

### Shortening/lengthening of elements

Now, for each element the shortening / lengthening can be calculated:

$$\Delta L = \frac{{NL}}{{EA}} \to \begin{array}{c}
{\Delta {L_{{\rm{AC}}}} =  - 0.025{\text{ m}}}\\
{\Delta {L_{{\rm{CE}}}} =  - 0.012{\text{ m}}}\\
{\Delta {L_{\rm{BE}}} = \cfrac{1}{{120}} \approx  - 0.00833{\text{ m}}}\\
{\Delta {L_{{\rm{CD}}}} = \cfrac{1}{{120}} \approx  - 0.00833{\text{ m}}}\\
{\Delta {L_{{\rm{DE}}}} = \cfrac{1}{{120}} \approx 0.00833{\text{ m}}}\\
{\Delta {L_{{\rm{AD}}}} = 0.018 - \cfrac{1}{{625}}{B_{\rm{h}}} = 0.018 - 0.0016{B_{\rm{h}}}{\text{ m}}}\\
{\Delta {L_{{\rm{DB}}}} = 0.006 - 0.0016{B_{\rm{h}}}{\text{ m}}}
\end{array}$$

### Displacement structure due to $20 \text{ kN}$

For now we'll ignore the shortening/lengethening due to $B_\text{h}$:

```{figure} ./intro_data/elong.svg
:align: center

Shortening/lengthening of elements
```

This gives the following Williot-diagram with a fixed $\text{AC}$:

```{figure} ./intro_data/williot.svg
:align: center

Williot diagram with fixed $\text{AC}$
```

Leading to the following displacements if $\text{AC}$ doesn't rotate:

| joint | Displacement due to $20 \text{ kN}$ with fixed $\text{AC}$ in horizontal direction → $\left( \text{mm}\right)$| Displacement due to $20 \text{ kN}$ with fixed $\text{AC}$ = in vertical direction ↓ $\left( \text{mm}\right)$|
| :-:|:-:|:-:|
|$\text{A}$|$0$|$0$|
|$\text{C}$|$-13$|$21$|
|$\text{D}$|$18$|$-12.5$|
|$\text{E}$|$-25$|$-55$|
|$\text{B}$|$24$|$-103$|

$\text{B}$ shouldn't move vertically, so this structure has to be rotated back with $\theta  \approx \cfrac{{103}}{{12000}} \approx 8.5476 \cdot {10^{ - 3}}{\text{ rad}}$ ⟳, leading to:

| joint | Displacement due to $\theta$ in horizontal direction → $\left( \text{mm}\right)$| Displacement due to $\theta$ in vertical direction ↓ $\left( \text{mm}\right)$|
| :-:|:-:|:-:|
|$\text{A}$|$0$|$0$|
|$\text{C}$|$34$|$26$|
|$\text{D}$|$0$|$51$|
|$\text{E}$|$34$|$77$|
|$\text{B}$|$0$|$103$|

Resulting in total displacements of:

| joint | Displacement due to in horizontal direction → $\left( \text{mm}\right)$| Displacement in vertical direction ↓ $\left( \text{mm}\right)$|
| :-:|:-:|:-:|
|$\text{A}$|$0$|$0$|
|$\text{C}$|$21$|$47$|
|$\text{D}$|$18$|$39$|
|$\text{E}$|$9$|$22$|
|$\text{B}$|$24$|$0$|

```{figure} ./intro_data/displaced.svg
:align: center

Displaced structure
```

### Displacement structure due to $B_\text{h}$

For the displacement due to $B_\text{h}$ in $\text{kN}$, the following Williot-diagram with a fixed $\text{AD}$ can be drawn:

```{figure} ./intro_data/williot2.svg
:align: center

Williot diagram with fixed $\text{AD}$
```
Leading to the following displacements if $\text{AD}$ doesn't rotate:

| joint | Displacement due to $B_\text{h}$ in horizontal direction → | Displacement due to $B_\text{h}$ in vertical direction ↓|
| :-:|:-:|:-:|
|$\text{A}$|$0$|$0$|
|$\text{C}$|$-0.8{B_{\rm{h}}}$|$-0.6{B_{\rm{h}}}$|
|$\text{D}$|$-1.6{B_{\rm{h}}}$|$0$|
|$\text{E}$|$-0.8{B_{\rm{h}}}$|$0.6{B_{\rm{h}}}$|
|$\text{B}$|$-3.2{B_{\rm{h}}}$|$2.4{B_{\rm{h}}}$|

Again, $\text{B}$ Shouldn't move vertically, so this structure has to be rotated back with $\theta = \cfrac{2.4{B_{\rm{h}}}}{{12000}} = 0.0002{B_{\rm{h}}}{\text{ rad}}$ ⟲, leading to: 

| joint | Displacement due to $\theta$ in horizontal direction → $\left( \text{mm}\right)$| Displacement due to $\theta$ in vertical direction ↓ $\left( \text{mm}\right)$|
| :-:|:-:|:-:|
|$\text{A}$|$0$|$0$|
|$\text{C}$|$-0.8 B_\text{h}$|$-0.6 B_\text{h}$|
|$\text{D}$|$0$|$-1.2B_\text{h}$|
|$\text{E}$|$-0.8 B_\text{h}$|$-1.8B_\text{h}$|
|$\text{B}$|$0$|$-2.4 B_\text{h}$|

Resulting in total displacements of:

| joint | Displacement due to in horizontal direction → $\left( \text{mm}\right)$| Displacement in vertical direction ↓ $\left( \text{mm}\right)$|
| :-:|:-:|:-:|
|$\text{A}$|$0$|$0$|
|$\text{C}$|$-1.6B_\text{h}$|$-1.2B_\text{h}$|
|$\text{D}$|$-1.6{B_{\rm{h}}}$|$-1.2B_\text{h}$|
|$\text{E}$|$-1.6B_\text{h}$|$-1.2B_\text{h}$|
|$\text{B}$|$-3.2B_\text{h}$|$0$|

```{figure} ./intro_data/displaced2.svg
:align: center

Displaced structure
```

## Solve statically indeterminate structure with compatibility conditions

Now, we can fill in the compatibility conditions:

$${u_{{\rm{B,h}}}} = 0 \to 0.024 - 0.0032{B_{\rm{h}}} = 0 \to {B_{\text{h}}} =  7.5{\text{ kN}}$$

### Section forces statically indeterminate structure

The section forces can be calculated by filling in the resulting $B_\text{h}$ in our previous expressions:

| Element | Normal force $\text{kN}$|
| :-:|:-:|
|$\text{AC}$|-18.75|
|$\text{CE}$|-7.5|
|$\text{BE}$|-6.25|
|$\text{CD}$|-6.25|
|$\text{DE}$|6.25|
|$\text{AD}$|3.75|
|$\text{DB}$|-3.75|

```{figure} ./intro_data/N-line.svg
:align: center

Normal force distribution
```

### Displacements statically indeterminate structure
Now, the displacements can be found as well by filling in the resulting $B_\text{h}$ in our previous expressions:

| joint | Displacement in horizontal direction → $\left( \text{mm}\right)$| Displacement in vertical direction ↓ $\left( \text{mm}\right)$|
| :-:|:-:|:-:|
|$\text{A}$|$0$|$0$|
|$\text{C}$|$9$|$38$|
|$\text{D}$|$6$|$29.833$|
|$\text{E}$|$-3$|$12.66$|
|$\text{B}$|$0$|$0$|

```{figure} ./intro_data/displaced3.svg
:align: center

Displaced structure
```