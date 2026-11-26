<!-- фрагмент: страницы PDF 126–136, строки исходного md 6437–7114 -->
<!-- page 126 -->
7

Asquith, G., and D. Krygowski, 2004, Log Interpretation, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 115-135.

# Log Interpretation

## GENERAL

As shown in the previous chapters, determining the porosity and true resistivity of a zone is the first step in converting the raw log data into estimated quantities of oil, gas, and water in a formation. These estimated quantities are used to evaluate a zone and to determine whether a well completion attempt is warranted. This chapter covers some of the different methods from which these estimates are derived. The methods discussed are: Archie water saturations ($S_w$ and $S_{xo}$) and the ratio method, quick-look technique, bulk volume water ($BVW$), and saturation crossplots (Pickett plots and Hingle plots). Determination of log-derived permeability ($K_e$) and shaly sand analysis are also discussed.

As important as this log-derived information is, however, it should not be applied without the inclusion of other data. This statement is, perhaps, obvious to the reader, but it can't be overemphasized. A geologist should always consider every item of relevant data, such as drill stem tests, sample shows, mud-log analysis, nearby production, etc., before making a decision to set pipe.

## SCANNING THE LOGS: A RECONNAISSANCE TECHNIQUE

It is an exceedingly rare log that contains more reservoir than nonreservoir, and when one is unfamiliar with an area or wants to broadly reconnoiter an area, a scanning technique that sorts reservoir from nonreservoir can be helpful, even with access to computer-aided processing. A good scanning technique not only identifies the reservoirs, but can also give the geologist hints as to potential pay and wet zones. Remember that in the interpretive process, the identification of wet zones is as important as the discovery of those containing hydrocarbons, because the com

comparison of the two helps clearly identify both the presence and amount of the hydrocarbons.

Figure 7.1 is a flowchart for one such scanning technique. Note that it has two paths, one for clastics and one for carbonates. In the clastic case, the resistivity log is the primary reconnaissance measurement because clastics tend to consist of reservoirs surrounded by shales of slowly varying resistivity. The changes in resistivity due to changes in fluid content of the reservoirs tend to stand out against this relatively constant background. On the carbonate path, on the other hand, formation resistivities tend to vary widely with changing rock types, and commonly there are few shales against which to measure changes. In this case, the porosity log is the primary reconnaissance measurement. By first finding the porous zones, those with the capacity to hold fluids (of any type) can be identified.

Figure 7.2 shows the details of a log interpretation, once zones of interest are identified, with references to the chapters in which the information is discussed.

## ARCHIE WATER SATURATIONS: $S_W$ AND $S_{XO}$

Water saturation ($S_w$) of a reservoir's uninvaded zone is calculated by the Archie (1942) formula:

$$
S_w = \left( \frac{a \times R_w}{R_t \times \phi^m} \right)^{\frac{1}{n}} \tag{7.1}
$$

where:

$S_w =$ water saturation of the uninvaded zone

$R_w =$ resistivity of formation water at formation temperature

$R_t =$ true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$\phi =$ porosity

$a =$ tortuosity factor (Table 1.1; Chapter 1)

115
<!-- page 127 -->
116

ASQUITH AND KRYGOWSKI

$m =$ cementation exponent (Table 1.1; Chapter 1)

$n =$ saturation exponent

The uninvaded zone's water saturation ($S_w$), determined by the Archie equation, is the most fundamental quantity used in log evaluation. But merely knowing a zone's water saturation ($S_w$) does not provide enough information to completely evaluate a zone's potential productivity. A geologist must also determine if:

- the water saturation is low enough for a water-free completion
the hydrocarbons are moveable
the zone is permeable
- there is an commercial volume of recoverable hydrocarbon reserves

Water saturation of a formation's flushed zone ($S_{xo}$) is also based on the Archie equation, but two variables are changed: mud filtrate resistivity ($R_{mf}$) in place of formation water resistivity ($R_w$) and flushed zone resistivity ($R_{xo}$) in place of uninvaded zone resistivity ($R_t$).

$$
S_{xo} = \left( \frac{a \times R_{mf}}{R_{xo} \times \phi^m} \right)^{\frac{1}{n}} \tag{7.2}
$$

where:

$S_{xo} =$ water saturation of the flushed zone

$R_{mf} =$ resistivity of the mud filtrate at formation temperature

$R_{xo} =$ shallow resistivity from a very shallow reading device, such as laterolog-8, microspherically focused log, or microlaterolog

$\phi =$ porosity

$a =$ tortuosity factor (Table 1.1; Chapter 1)

$m =$ cementation exponent (Table 1.1; Chapter 1)

$n =$ saturation exponent

Water saturation of the flushed zone ($S_{xo}$) can be used as an *indicator of hydrocarbon moveability*. For example, if the value of $S_{xo}$ is much larger than $S_w$, then hydrocarbons in the flushed zone have probably been moved or flushed out of the zone nearest the borehole by the invading drilling fluids ($R_{mf}$).

## Ratio Method

The ratio method identifies hydrocarbons from the difference between water saturations in the flushed zone ($S_{xo}$) and the uninvaded zone ($S_w$). When the uninvaded zone form of Archie's equation (Equation 7.1) is divided by the flushed zone form (Equation 7.2), the following results:

$$
\left( \frac{S_w}{S_{xo}} \right)^2 = \frac{R_{xo} / R_t}{R_{mf} / R_w} \tag{7.3}
$$

where:

$S_w =$ water saturation in the uninvaded zone

$S_{xo} =$ water saturation in the flushed zone

$R_{xo} =$ formation's shallow resistivity from a measurement such as laterolog-8, microspherically focused log, or microlaterolog

$R_t =$ true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$R_{mf} =$ resistivity of the mud filtrate at formation temperature

$R_w =$ resistivity of formation water at formation temperature

When $S_w$ is divided by $S_{xo}$, the formation factor ($F = a/\phi^m$) is cancelled out of the equation because the same formation factor is used to calculate both $S_w$ and $S_{xo}$. This can be very helpful in log analysis because, from the ratio $(R_{xo}/R_t)/(R_{mf}/R_w)$, the geologist can determine a value for both the moveable hydrocarbon index ($S_w/S_{xo}$) and water saturation by the ratio method without knowing porosity. Therefore, a geologist can still derive useful formation evaluation log parameters even though porosity logs are unavailable.

The moveable hydrocarbon index by the ratio method is:

$$
\frac{S_w}{S_{xo}} = \left( \frac{R_{xo} / R_t}{R_{mf} / R_w} \right)^{\frac{1}{2}} \tag{7.4}
$$

where:

$S_w/S_{xo} =$ moveable hydrocarbon index

$R_{xo} =$ shallow resistivity from measurements such as laterolog-8, microspherically focused log, or microlaterolog

$R_t =$ true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$R_{mf} =$ resistivity of mud filtrate at formation temperature

$R_w =$ resistivity of formation water at formation temperature

The cementation exponent ($n$) is assumed to be 2.0

If the ratio $S_w/S_{xo}$ is equal to or greater than 1.0, then hydrocarbons were not moved during invasion. This is true regardless of whether or not a formation contains hydrocarbons. Whenever the ratio $S_w/S_{xo}$ is less than 0.7 for sandstones or less than 0.6 for carbonates, moveable hydrocarbons are indicated (Schlumberger, 1972).

To determine water saturation by the ratio method
<!-- page 128 -->
Log Interpretation 117

$(S_{wr})$, you must know the flushed zone's water saturation. In the flushed zone of formations with moderate invasion and average residual hydrocarbon saturation, the following relationship normally works well:

$$S_{xo} = (S_w)^{\frac{1}{2}} \tag{7.5}$$

where:

$S_{xo}$ = water saturation of the flushed zone

$S_w$ = water saturation of the uninvaded zone

Substituting Equation 7.5 in Equation 7.4 and solving for $S_w$, the ratio method water saturation ($S_{wr}$) is:

$$S_{wr} = \left( \frac{R_{xo} / R_t}{R_{mf} / R_w} \right)^{\frac{5}{8}} \tag{7.6}$$

or:

$$S_{wr} = \left( \frac{R_{xo} / R_t}{R_{mf} / R_w} \right)^{0.625} \tag{7.7}$$

where:

$S_{wr}$ = moveable hydrocarbon index

$R_{xo}$ = shallow resistivity from measurements such as laterolog-8, microspherically focused log, or microlaterolog

$R_t$ = true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$R_{mf}$ = resistivity of mud filtrate at formation temperature

$R_w$ = resistivity of formation water at formation temperature

To use the ratio method in an interpretation process, the water saturation of the uninvaded zone should be calculated by both the Archie equation ($S_{wa}$) and the ratio method ($S_{wr}$). The following observations can be made:

1. If $S_{wa} \sim S_{wr}$, the assumption of a step-contact invasion profile is indicated to be correct, and all values determined ($S_w$, $R_t$, $R_{xo}$, and $d_t$) are correct.

2. If $S_{wa} > S_{wr}$, then the value for $R_{xo}/R_t$ is too low. $R_{xo}$ is too low because invasion is very shallow, or $R_t$ is too high because invasion is very deep. Also, a transition-type invasion profile might be indicated and $S_{wa}$ is considered a good value for the zone's actual water saturation.

3. If $S_{wa} < S_{wr}$, then the value for $R_{xo}/R_t$ is too high. $R_{xo}$ is too high because of the effect of adjacent, high-resistivity beds, or $R_t$ estimated from the deep resistivity measurement is too low because $R_{xo}$ is less than $R_t$. Also, an annulus-type invasion profile might be indicated and/or $S_{xo} < S_w^{1/5}$ (from Equation 7.5). In this case, a more accurate value for water saturation

can be estimated using the following equation (from Schlumberger, 1977):

$$(S_w)_{COR} = S_{wa} \times \left( \frac{S_{wa}}{S_{wr}} \right)^{0.25} \tag{7.8}$$

where:

$(S_w)_{COR}$ = corrected water saturation of the uninvaded zone

$S_{wa}$ = water saturation of the uninvaded zone (Archie method)

$S_{wr}$ = water saturation of the uninvaded zone (ratio method)

4. If $S_{wa} < S_{wr}$, the reservoir might be a carbonate with moldic (i.e., oomoldic, fossil-moldic, etc.) porosity and low permeability.

### QUICK-LOOK METHODS

#### General

Quick-look methods are helpful to the geologist because they provide flags, or indicators, that point to possible hydrocarbon zones requiring further investigation. The four quick-look methods discussed here are:

- $R_{xo}/R_t$
- apparent water resistivity ($R_{wa}$)
- conductivity-derived porosity
- Wet resistivity ($R_o$)

#### $R_{xo}/R_t$

The $R_{xo}/R_t$ technique relies on the comparison of the resistivity ratio, plotted as a curve on the log display, to the SP curve.

#### Procedure

1. Calculate the $R_{xo}/R_t$ ratio from the deep and shallow reading resistivity measurements;
2. Plot the ratio in the same track as the SP, and look for the following patterns.

#### Patterns to observe

1. In a shale, the ratio is relatively constant, like the SP, and usually close to 1.
2. In a water-bearing zone, the $R_{xo}/R_t$ ratio tracks the SP.
3. In a hydrocarbon-bearing zone, the $R_{xo}/R_t$ ratio moves away from the SP [a deflection to the right for the case of a normal (negative) SP].
<!-- page 129 -->
118

ASQUITH AND KRYGOWSKI

Basis for the technique

From Chapter 2, the equation relating the SP to fluid resistivities is:

$$SP = -K \times \log\left(\frac{R_{mf}}{R_w}\right) \tag{7.9}$$

In water-bearing zones:

$$R_{xo} = F \times R_{mf} \quad (\text{flushed zone}) \tag{7.10}$$

$$R_o = F \times R_w \quad (\text{uninvaded zone}) \tag{7.11}$$

Solving Equations 7.2 and 7.3 for $R_{mf}$ and $R_w$ respectively, and substituting the results in Equation 7.1 yields:

$$SP = -K \times \log\left(\frac{R_{xo}}{R_o}\right) \tag{7.12}$$

The $R_{xo}/R_o$ ratio is then related to the SP through a constant. Since $R_o$ is just a special case of $R_t$ ($R_o$ is the resistivity in the undisturbed, water-bearing zone), $R_t$ can be substituted for $R_o$ for the more general case. In water-bearing intervals, the $R_{xo}/R_t$ ratio parallels the response of the SP, and both curves move in the same direction from their respective baseline values. In a hydrocarbon-bearing interval, while the SP still responds to the differences in connate water and mud filtrate resistivities and moves accordingly, the $R_{xo}/R_t$ ratio decreases (because of increasing $R_t$) and the $R_{xo}/R_t$ curve moves away from the SP.

The $R_{xo}$ curve usually used for the ratio is derived from a shallow-reading measurement, such as a microspherically focused log or a microlaterolog. The $R_t$ curve is derived from a deep-reading measurement such as the deep induction log or deep laterolog. In practice, especially when the ratio is calculated and displayed as part of the logging job, the measurements are normally used without any environmental corrections being applied.

### Apparent water resistivity ($R_{wa}$)

The $R_{wa}$ technique relies on the comparison of calculated values of water resistivity between intervals in a well. This comparison can be made between different zones or within the same zone if a water-hydrocarbon contact is suspected in that zone. The assumption is that this lowest value of $R_{wa}$ is the closest approximation to the true formation water resistivity ($R_w$) and that values of $R_{wa}$ greater than the minimum value are indicative of the presence of hydrocarbons. A water saturation can also be calculated from the values of $R_{wa}$.

Procedure

1. Calculate an apparent water resistivity ($R_{wa}$) from the porosity and uninvaded zone resistivity measurements.
2. Look for the lowest value of $R_{wa}$ in a porous and permeable zone and compare it to the values of $R_{wa}$ calculated in the other zones.
3. If desired, an Archie water saturation can be calculated from the $R_{wa}$ values in the compared zones.

Patterns to observe

1. The zone with the lowest value of $R_{wa}$ is the most likely to be water-bearing, and the value of $R_{wa}$ is closest to the actual value of $R_w$ in the formation.
2. Zones with values of $R_{wa}$ greater than the minimum observed are likely to have some hydrocarbon saturation.

Interpretation pitfalls

The $R_w$ values in the zones that are compared are assumed to be the same.

In low-porosity zones (less than about 10% porosity), the $R_{wa}$ value is lower than the actual $R_w$ value.

Basis for the technique

Recall from Chapter 1 that

$$R_o = F \times R_w \tag{7.13}$$

and

$$F = \frac{a}{\phi^m} \tag{7.14}$$

Combining Equations 7.5 and 7.6, and solving for $R_w$ yields:

$$R_w = \frac{R_o \times \phi^m}{a} \tag{7.15}$$

From Equation 7.7 above, define apparent water resistivity ($R_{wa}$) as:

$$R_{wa} = \frac{R_t \times \phi^m}{a} \tag{7.16}$$

When a given zone is water bearing, $R_t$ reverts to the water-bearing resistivity ($R_o$) and $R_{wa}$ equals $R_w$. If the zone contains hydrocarbons, $R_t$ is greater than $R_o$, and $R_{wa}$ is greater than $R_w$. By comparing a number of zones (or different depths in the same zone, where a water-hydrocarbon contact is suspected) and assuming the zone with the lowest value of $R_{wa}$ is wet, the minimum value of $R_{wa}$ can be used as an estimate for the value of $R_w$ in all the zones being considered. If the zone with the minimum $R_{wa}$ value actually contains
<!-- page 130 -->
Log Interpretation

119

some hydrocarbons, then the other zones contain even more hydrocarbons than anticipated.

In practice, especially when calculated and displayed as a curve during a logging job, the following values are used for simplicity: $a = 1.0$, $m = 2.0$. The deep induction log or deep laterolog is used as $R_t$, usually without any environmental corrections. Porosity is usually derived from the sonic or density log using the proper matrix and fluid parameters for the formations to be encountered. If available in real time during logging, the neutron-density crossplot porosity should be used for the best estimate of porosity.

An Archie water saturation can also be calculated from the ratio of the $R_{wa}$ values.

$$S_w = \sqrt{\frac{R_{wa\ minimum}}{R_{wa\ zone}}} \tag{7.17}$$

where the cementation exponent ($n$) in the equation above is assumed to be 2.

A shortcut to the saturation calculation, used as a scanning aid, is:

- ($R_{wa\ zone}/R_{wa\ minimum}$) = 3 yields $S_w = 0.58$;
- ($R_{wa\ zone}/R_{wa\ minimum}$) = 4 yields $S_w = 0.50$;
- ($R_{wa\ zone}/R_{wa\ minimum}$) = 5 yields $S_w = 0.45$.

Where $a = 1.0$ and $m = 2.0$.

### Conductivity-derived porosity (also referred to as resistivity-porosity)

Although this technique originated with the use of the conductivity curve (Dresser Atlas, 1975), the conductivity curve is now rarely presented on log displays, and the technique is described here using the resistivity measurement.

This technique calculates a porosity from Archie's equation, using the form of the equation for water-bearing zones ($S_w = 1$). The porosity values are generated as a curve and are normally displayed in the same track as the SP, scaled from high porosity values on the left to low porosity values on the right.

### Procedure

1. Calculate the porosity from Archie's equation (assuming $S_w = 1.0$), using the uninvaded zone resistivity measurement.
2. Compare the curve values and the relative position of the curve in porous and permeable zones.
3. If desired, an Archie water saturation can be calculated by comparing the conductivity-derived porosity

ty to porosity from one of the porosity measurements (sonic, density, or neutron).

### Patterns to observe

1. In water-bearing zones, the conductivity-derived porosity is high and approximately equal to the true formation porosity.
2. In zones that contain hydrocarbons, the conductivity-derived porosity is low, lower than the true formation porosity.

### Interpretation pitfalls

The choice of an incorrect value for $R_w$ would change the value of conductivity-derived porosity, and might make its comparison to true formation porosity inaccurate. It would not, however, change the results of comparison of the curve values in different zones.

### Basis for the technique

From Chapter 1, Archie's equation can be solved for porosity:

$$\phi = \left(\frac{a \times R_w}{R_t \times S_w^n}\right)^{\frac{1}{m}} \tag{7.18}$$

If the water-bearing case is considered, where $S_w = 1$, the equation reduces to:

$$\phi = \left(\frac{a \times R_w}{R_t}\right)^{\frac{1}{m}} \tag{7.19}$$

By using the form of the equation above (7.19), the water-filled porosity is determined. Where the formation is actually water filled, $R_t$ reverts to the water-bearing resistivity ($R_o$). The porosity calculated from this equation is close to the actual formation porosity, assuming that the parameters in the equation are close to the actual formation parameters. When the formation contains hydrocarbons, $R_t$ is greater than $R_o$, and the calculated porosity is less than the actual formation porosity.

Traditionally this curve has been plotted in the same log track as the SP curve, and its movement compared to the SP. It can also be plotted in the same track as a porosity curve from one of the porosity tools, where decreases in conductivity-derived porosity with respect to the porosity curve indicate the presence of hydrocarbons.

Water saturation can be estimated by the following equation:

$$S_w = \frac{\phi_{conductivity}}{\phi_{actual}} \tag{7.20}$$
<!-- page 131 -->
120

ASQUITH AND KRYGOWSKI

### Wet resistivity ($R_o$)

The wet-resistivity curve ($R_o$) is one of the oldest quick-look techniques. Unlike the other curves, which tend to be compared to the SP curve, it is plotted as an overlay on the resistivity curve.

### Procedure

1. Calculate $R_o$ from the porosity and an estimate of formation water resistivity ($R_w$).
2. Plot $R_o$ as a curve at the same scale as the resistivity curves and compare the values to the value of the deep-resistivity measurement.
3. If desired, an Archie water saturation can be calculated in any zone from the values of $R_o$ and the deep resistivity measurement.

### Patterns to observe

1. In water-bearing zones, $R_o$ and the deep resistivity should overlay.
2. In hydrocarbon-bearing zones, the deep resistivity is higher than $R_o$, with the separation increasing with increasing hydrocarbon saturation.

### Interpretation pitfalls

If the value of $R_w$ chosen to calculate $R_o$ is incorrect, the curves would not align in water-bearing zones.

### Basis for the technique

Recall from chapter 1 that:

$$R_o = F \times R_w = \frac{a \times R_w}{\phi^m} \tag{7.21}$$

$R_o$ is then calculated from a porosity measurement, usually the sonic or density, with an estimate of $R_w$, $a$, and $m$. The curve can be generated and displayed during the logging job.

### BULK VOLUME WATER

The product of a formation's water saturation ($S_w$) and its porosity ($\phi$) is the bulk volume of water ($BVW$).

$$BVW = S_w \times \phi \tag{7.22}$$

where:

$BVW$ = bulk volume water

$S_w$ = water saturation of uninvaded zone

$\phi$ = porosity

If values for bulk volume water, calculated at several depths in a formation, are constant or very close to

constant, they indicate that the zone is of a single rock type and at irreducible water saturation ($S_{w\ irr}$). When a zone is at irreducible water saturation, water in the uninvaded zone ($S_w$) does not move because it is held on grains by capillary pressure. Therefore, hydrocarbon production from a zone at irreducible water saturation should be water free (Morris and Biggs, 1967).

A formation not at irreducible water saturation ($S_{w\ irr}$) exhibits wide variations in bulk volume water values. The Buckles plot (Buckles, 1965) is a graph of porosity ($\phi$) versus $S_w$. Points of equal $BVW$ form hyperbolic curves across this plot. Figure 7.3 illustrates Buckles plots using data from three wells in the Ordovician Red River B-zone, Beaver Creek Field, North Dakota. If $BVW$ is plotted using data from a formation at irreducible water saturation, the points fall along a single hyperbolic curve (Figure 7.3a). If the data come from reservoirs with higher percentages of produced water, the points are more scattered (Figures 7.3b and 7.3c).

Because the amount of water a formation can hold by capillary pressure increases with decreasing grain size, the bulk volume water also increases with decreasing grain size. Table 7.1 illustrates the relationship of bulk volume water values to decreasing grain size and lithology.

Table 7.1. Bulk volume water ($BVW$) as a function of grain size and lithology. A comparative chart.

|  Lithology | Grain Size (millimeters) | Bulk Volume Water ($BVW$)  |
| --- | --- | --- |
|  *Clastics*  |   |   |
|  Coarse | 1.0 to 0.5 | 0.02 to 0.025  |
|  Medium | 0.5 to 0.25 | 0.025 to 0.035  |
|  Fine | 0.25 to 0.125 | 0.035 to 0.05  |
|  Very Fine | 0.125 to 0.062 | 0.05 to 0.07  |
|  Silt | < 0.062 | 0.07 to 0.09  |
|  *Carbonates*  |   |   |
|  Vuggy |   | 0.005 to 0.015  |
|  Vuggy and intercrystalline (intergranular) |   | 0.015 to 0.025  |
|  Intercrystalline |   | 0.025 to 0.04  |
|  Chalky |   | 0.05  |

The bulk volume water values for carbonates should be used only as a very general guide to different types of porosity.
<!-- page 132 -->
Log Interpretation 121

# SATURATION CROSSPLOTS

Saturation crossplots, also called resistivity-porosity crossplots (or specifically, Pickett plots and Hingle plots) are similar to the porosity crossplots discussed in Chapter 4. They are x-y plots of log data from which quantities of interest are derived; in this case, that quantity is water saturation ($S_w$). Both the Pickett and Hingle methods are essentially graphical solutions to the Archie saturation equation. They were created before the use of computers to aid log interpretation. These techniques minimize the number of calculations that must be done and aid the comparison of potentially productive zones. With the advent of early (mostly nongraphic) log-interpretation software, their use declined, but this decline was reversed as people realized the power of the techniques to use the ability of the human mind to recognize patterns in data. These techniques are currently regarded as necessary components of full-functioned computer-based log-interpretation systems.

## Pickett Crossplot Method

The Pickett plot (Pickett, 1966, 1973) is one of the simplest and most effective crossplot methods in use. This technique estimates water saturation and can also help determine:

- formation water resistivity ($R_w$)
- cementation factor ($m$)
- matrix parameters for sonic and density logs ($\Delta t_{ma}$ and $\rho_{ma}$)

The Pickett method is based on the observation that true resistivity ($R_t$) is a function of porosity ($\phi$), water saturation ($S_w$), and cementation exponent ($m$). It is actually a graphical solution of Archie's equation in terms of resistivity. Archie's equation (Equation 7.1) is solved for resistivity:

$$R_t = \frac{a \times R_o}{\phi^m \times S_w^n} \tag{7.23}$$

Taking the logarithm of the equation produces:

$$\log(R_t) = \log(a \times R_w) - m \log(\phi) - n \log(S_w) \tag{7.24}$$

If the zone is water-bearing, $S_w = 1$, $\log(S_w) = 0$, and the equation reduces to:

$$\log(R_t) = \log(a \times R_w) - m \log(\phi) \tag{7.25}$$

This form of the equation ($y = b + mx$) indicates that by plotting $R_t$ on the y-axis (on a logarithmic scale) against porosity ($\phi$) on the x-axis (on a logarith-

mic scale), one can determine the product ($a \times R_w$) from intercept of the line (b), and the cementation exponent ($m$) from the slope of the line ($m$). In practice, the resistivity ($R_t$) is usually plotted on the x-axis and the porosity ($\phi$) on the y-axis (Figure 7.4). This convention stems from the availability of full-logarithmic graph paper (both scales logarithmic) at the time Pickett developed the technique. The best format to use (for the best data resolution) is two decades for porosity (0.01 to 1.0, or 1% to 100%) and three decades for the resistivity (0.1 to 100, or 1 to 1000). The only 2-by-3 full-logarithmic paper available was constructed with 2 decades on the y-axis and 3 decades on the x-axis so the plot was modified to fit the paper (G. R. Pickett, personal communication).

Using the convention driven by graph-paper availability, the equation becomes:

$$\log(\phi) = \log(a \times R_w) - \frac{1}{m} \log(R_t) - n \log(S_w) \tag{7.26}$$

Plotting a mixture of water-bearing and hydrocarbon-bearing points on a Pickett plot results in the following attributes (as shown in Figure 7.4):

- Water-bearing points of different porosities plot along a straight line with a slope of ($-1/m$) and an intercept (at porosity = 1.0) of ($a \times R_w$). From this line, the cementation exponent ($m$) can be determined, and if the tortuosity factor ($a$) is known (or can be estimated), $R_w$ can be predicted. This is the water-bearing, or $R_o$, line.
- Hydrocarbon-bearing points lie away from the line, moved horizontally to the right from the water-bearing line by their increased resistivity. The horizontal distance of a point from the water-bearing line depends on the water saturation ($S_w$) of that point. If the saturation exponent ($n$) is known (or can be estimated), the water saturation can be determined. Lines of constant water saturation lie parallel to the water-bearing line.

The power in the Pickett plot is that water resistivity ($R_w$) and cementation exponent ($m$) can be estimated from the data, rather than having to be derived from local knowledge or from expensive core measurements.

Although porosity is now normally plotted on the Pickett plot, Pickett originally used two other quantities:

($\rho_b - \rho_{ma}$) instead of the density porosity

where:

$\rho_b$ = formation bulk density (from the log)

$\rho_{ma}$ = formation matrix density
<!-- page 133 -->
122

ASQUITH AND KRYGOWSKI

and:

$$(\Delta t - \Delta t_{ma})$$ instead of the sonic porosity where:

$$\Delta t =$$ formation sonic travel time (from the log)

$$\Delta t_{ma} =$$ formation matrix travel time

Both quantities are the numerators in porosity equations $$(\rho_b - \rho_{ma})$$ from the density porosity equation (Chapter 4, Equation 4.7), and $$(\Delta t - \Delta t_{ma})$$ from the Wyllie time-average sonic equation (Chapter 4, Equation 4.1). The quantities are plotting shortcuts to avoid the calculation of porosity, but they serve another purpose as well. If there is a range of porosities in the zones defining the water-bearing line on the Pickett plot, and if the matrix value is chosen correctly, the line is straight. If the chosen matrix value is either too high or too low, the line is curved. Thus, with a spread of good data in the water-bearing zone, the proper matrix value can be chosen by trial and error by modifying the matrix value until the water-bearing line is straight and not curved.

The water saturation of a point plotting away from the water-bearing line can be determined by the equation:

$$S_w = \left(\frac{R_o}{R_t}\right)^{\frac{1}{n}} \tag{7.27}$$

In practice, this means reading the resistivity of the point $$(R_t)$$ and the resistivity of the water-bearing line $$(R_o)$$ at the same porosity value as the point, estimating a value for saturation exponent (n) and making the calculation.

The table below can be used to draw saturation lines on a Pickett plot, as a reference. The technique is:

- At some value of porosity (0.10 is often convenient), note the resistivity value of the $$R_o$$ line.
- Multiply that resistivity value by the factors below, and plot those values on the Pickett plot at the same porosity.
- Draw the saturation lines parallel to the water-bearing line, with each line going through the calculated points.
- Those parallel lines can be labeled with the value of water saturation shown. Note that the lines are for a saturation exponent (n) of 2.0.

In its fullest use, then, the Pickett plot can be used to determine formation water resistivity ($$R_w$$), cementation exponent (m), and formation matrix values ($$\rho_{ma}$$ or $$\Delta t_{ma}$$). As expected, there are assumptions to the interpretation. The prime assumption is that in the zones being compared, all the parameters (matrix value, a, m, n, and $$R_w$$) do not change.

Table 7.2. Factors for positioning water-saturation lines on Pickett and Hingle plots.

|  Multiplier | $$S_w$$ (for n = 2.0)  |
| --- | --- |
|  1.56 | 0.80  |
|  2.04 | 0.70  |
|  2.78 | 0.60  |
|  4 | 0.50  |
|  6.25 | 0.40  |
|  11.11 | 0.30  |
|  25 | 0.20  |

### Hingle Crossplot Method

The oldest of the resistivity-porosity crossplot methods that can be used to determine water saturation ($$S_w$$) is the Hingle (1959) plot. As in other crossplot techniques, a significant benefit of Hingle's technique is that a value for water saturation ($$S_w$$) can be determined even if matrix properties ($$\rho_{ma}$$ or $$\Delta t_{ma}$$) of a reservoir are unknown. This is also true if a reservoir's water resistivity ($$R_w$$) is unknown.

As with the Pickett plot, the Hingle plot seeks to plot resistivity against porosity. Plotting resistivity against porosity on linear scales produces a family of nonlinear trends. By solving Archie's equation (Equation 7.1) in the following form, the nonlinear trends become straight lines (Bassiouni, 1994):

$$\left(\frac{a}{R_t}\right)^{\frac{1}{m}} = \left(\frac{S_w^n}{R_w}\right)^{\frac{1}{m}} \times \phi \tag{7.28}$$

While porosity is plotted on a linear scale, the resistivity is plotted on a very nonlinear scale. In practice, the resistivity is plotted on a grid that has been constructed for specific values of tortuosity factor (a) and cementation exponent (m). The grid constructed using a = 1.0 and m = 2.0 is usually used for sandstones (Figure 7.5), and the grid constructed using a = 0.62 and m = 2.15 is used for carbonates (Figure 7.6). Using the constructed grids, resistivity values can be plotted directly on the graph without the need for any calculations.

Plotting a mixture of water-bearing and hydrocarbon-bearing points on a Hingle plot results in the following attributes (as shown in Figure 7.7):

- Water-bearing points of different porosities plot along a straight line. The x-intercept of the line (where conductivity is zero and resistivity is infinite) occurs at the point where porosity is
<!-- page 134 -->
Log Interpretation

123

zero. If the bulk density or acoustic travel time of the formation, instead of the porosity, is plotted along the x-axis, the x-intercept predicts the matrix value (matrix density or matrix travel time) of the formation. The line extends to the northeast quadrant (i.e., upper right) from its x-intercept.

- Hydrocarbon-bearing points lie below the line of 100% water saturation, moved downward from the water-bearing line by their increased resistivity. The vertical distance from a point to the water-bearing line depends on the water saturation ($S_w$) of that point. If the saturation exponent ($n$) is known (or can be estimated), the water saturation can be determined. Lines of decreasing water saturation radiate from the x-axis intercept and spread like a fan toward the right side of the chart.

As with the Pickett plot, the Hingle plot allows the interpreter to predict some of the parameters from the logs rather than estimating them by other methods. The formation water resistivity ($R_w$) can be estimated by choosing any point along the water-bearing line. The point's resistivity ($R_o$) and porosity can be read from the plot, and values of tortuosity factor ($a$) and cementation exponent ($m$) are assumed based on the chart that is chosen. Formation water resistivity is then:

$$R_w = \frac{R_o \times \phi^m}{a} \tag{7.29}$$

By plotting the bulk density ($\rho_b$) or sonic travel time ($\Delta t$) values on the x-axis, rather than the porosity, the matrix density or matrix travel time ($\rho_{ma}$ or $\Delta t_{ma}$) can be estimated. If there is a sufficient range of porosities used to determine the water-bearing line, the line can be extrapolated to the zero-conductivity value (the bottom of the chart). The value of this intercept is the matrix value for the porosity equation. On Figure 7.5 or Figure 7.6, the placement of the zero porosity point is arbitrary. If porosity is plotted on the x-axis, setting the zero porosity point at the left side of the plot makes the most sense. If $\rho_b$ or $\Delta t$ is used, the anticipated zero porosity point (the anticipated matrix value) could be displaced from the lower left corner if the matrix value is different than the expected matrix value. Regardless of the values used on the x-axis (porosity, $\rho_b$, or $\Delta t$), the values increase from left to right.

The water saturation of a point plotting away from the water-bearing line can be determined by Equation 7.26. In practice, this means reading the resistivity of the point ($R_t$) and the resistivity of the water-bearing line ($R_o$) at the same porosity value as the point, esti-

mating a value for saturation exponent ($n$), and making the calculation.

Table 7.2, previously used for the Pickett plot, can be used to draw saturation lines on a Hingle plot. The technique is:

- At some value of porosity (0.10 is often convenient), note the resistivity value of the $R_o$ line.
- Multiply that resistivity value by the factors in Table 7.2, and plot those values on the Hingle plot at the same porosity.
- Draw the saturation lines to intersect the water-bearing line at the zero porosity point on the x-axis, with each line going through the calculated points.
- Those lines can be labeled with the value of water saturation shown. Note that the lines are for a saturation exponent ($n$) of 2.0.

In routine analyses, many people favor one of the crossplots over the other, as a matter of personal preference or experience. Bassiouni (1994), however, describes an iterative technique using both plots to refine the estimates of the matrix values and cementation exponents in areas where both are unknown. Table 7.3 lists advantages and limitations of both plots.

### PERMEABILITY FROM LOGS

Log-derived permeability formulas are only valid for estimating permeability in formations at irreducible water saturation (Schlumberger, 1977). When a geologist evaluates a formation by using log-derived permeability formulas, the permeability values, if possible, should be compared with values of nearby producing wells from the same formation. Productivity estimates can be based on log-derived permeabilities if the formation evaluated is compared with both good and poor production histories in these nearby wells. By using comparisons of log-derived permeabilities from several wells, a geologist is not using an absolute value for log-derived permeability.

Four methods for calculating log-derived permeability are discussed here. Before these formulas can be applied, a geologist must first determine whether or not a formation is at irreducible water saturation. Whether or not a formation is at irreducible water saturation depends upon bulk volume water values ($BVW = S_w \times \phi$). When the bulk volume water values of a formation are constant (Figure 7.3a), the zone is at irreducible water saturation. If the values are not constant, a zone is not at irreducible water saturation (Figures 7.3b and 7.3c), and the estimates of permeability are suspect.
<!-- page 135 -->
124

ASQUITH AND KRYGOWSKI

Table 7.3. Advantages and Limitations of Pickett and Hingle plots (after Bassiouni, 1994).

|   | *Pickett plots* | *Hingle plots*  |
| --- | --- | --- |
|  Advantages | Water saturation can be predicted without prior knowledge of $R_w$, $a$, or $m$. $R_w$ is directly predicted (if tortuosity factor ($a$) is known or estimated) from the intercept of the water-bearing line at a porosity of 1 ($\phi = 100\%$). Cementation exponent ($m$) is directly predicted from the slope of the water-bearing line. When using the plot by hand, the graph paper to be used (full logarithmic) is readily available. | Water saturation can be predicted without prior knowledge of $R_w$, $\rho_{ma}$ or $\Delta t_{ma}$, $\rho_{ma}$ or $\Delta t_{ma}$ can be directly predicted from the intercept of the water-bearing line at a conductivity of zero (a resistivity of infinity).  |
|  Limitations | Values for $\rho_{ma}$ and $\Delta t_{ma}$ must be assumed (although in cases with a wide range of porosities in the water-bearing zone, the matrix values can be estimated from the water-bearing line). | Values for tortuosity factor ($a$) and cementation exponent ($m$) must be assumed. To use the plot, the resistivity parameter has to be calculated or a special graph paper used.  |
|  Limitations for both techniques | A wide range of porosity must be present to positively determine a water-bearing line. Formation lithology and water resistivity must be constant over the intervals compared in the plot.  |   |

Table 7.4. Data for use with Pickett plot (Figure 7.4) and Hingle plot (Figure 7.7). Morrow Sandstone, Cimarron County, Oklahoma.

|  Zone number | Depth (ft) | $\rho_b$ (g/cm³) | $\phi_D$ (decimal) | $R_t$ (ohm-m)  |
| --- | --- | --- | --- | --- |
|  1 | 4400 | 2.38 | 0.163 | 1.7  |
|  2 | 4402 | 2.44 | 0.127 | 2.1  |
|  3 | 4410 | 2.35 | 0.181 | 1.3  |
|  4 | 4414 | 2.42 | 0.139 | 1.6  |
|  5 | 4426 | 2.42 | 0.139 | 1.8  |
|  6 | 4430 | 2.33 | 0.194 | 1.0  |
|  7 | 4438 | 2.30 | 0.212 | 0.9  |
|  8 | 4536 | 2.30 | 0.212 | 40  |
|  9 | 4540 | 2.30 | 0.212 | 45  |
|  10 | 4546 | 2.30 | 0.212 | 40  |

## Wyllie and Rose (1950)

This method for determining permeability utilizes a chart (Figure 7.8) or the two forms of the following formula:

$$
K = \left( 250 \times \frac{\phi^3}{S_{\text{wirr}}} \right)^2 \text{ (medium-gravity oils)} \tag{7.30}
$$

$$
K = \left( 79 \times \frac{\phi^3}{S_{\text{wirr}}} \right)^2 \text{ dry gas)} \tag{7.31}
$$

where:

$K =$ permeability in millidarcys

$\phi =$ porosity

$S_{\text{wirr}} =$ water saturation ($S_w$) of a zone at irreducible water saturation

## Timur (1968)

$$
K = \left( \frac{93 \times \phi^{2.2}}{S_{\text{wirr}}} \right)^2 \tag{7.32}
$$

## Coates and Dumanoir (1973)

A more complex method for calculating permeability is the Coates and Dumanoir (1973) formula. Unlike the Wyllie and Rose (1950) formulas, hydrocarbon density is explicitly part of the equation, instead of being indirectly accounted for by changing a constant. The following data are required to calculate permeability by the Coates and Dumanoir formula.

$R_w =$ formation water resistivity at formation temperature

$R_{t\,irr} =$ true formation resistivity from a formation at irreducible water saturation
<!-- page 136 -->
Log Interpretation

125

$\rho_{h} =$ hydrocarbon density in $\mathrm{g / cm^3}$

$\phi =$ porosity

A first step in the Coates and Dumanoir permeability formula is calculation of values for two constants: $C$ and $W$.

$$
C = 23 + 465 \times \rho_{h} - 188 \times \rho_{h}^{2} \tag{7.33}
$$

where:

$C =$ constant in Coates and Dumanoir permeability formula

$\rho_{h} =$ hydrocarbon density in $\mathrm{g / cm^3}$

$$
W = \left\{(3.75 - \phi) + \left[ \frac{(\log(R_{w} / R_{t \text{ irr}}) + 2.2)^{2}}{2.0} \right] \right\}^{\frac{1}{2}} \tag{7.34}
$$

where:

$W =$ constant in Coates and Dumanoir permeability formula

$\phi =$ porosity

$R_{w} =$ formation water resistivity at formation temperature

$R_{t \text{ irr}} =$ deep resistivity from a zone at irreducible water saturation ($S_{w \text{ irr}}$)

Once determined, the constants $C$ and $W$ can be used to calculate permeability.

$$
K = \left[ \frac{C \times \phi^{2W}}{W^{4} \times (R_{w} / R_{t \text{ irr}})} \right]^{2} \tag{7.35}
$$

where:

$K =$ permeability in millidarcys (md)

$C =$ constant based on hydrocarbon density

$W =$ constant

$\phi =$ porosity

$R_{t \text{ irr}} =$ deep resistivity from a zone at irreducible water saturation ($S_{w \text{ irr}}$)

$R_{w} =$ formation water resistivity at formation temperature

## SHALY SAND ANALYSIS

Not long after the work of Archie and others in devising a method to quantify water saturation from logs, it became clear that there were limitations to the method, especially in formations containing shale and/or clay and commonly referred to as *shaly sands*. The early literature tended to refer to the formations as containing *shale*, and a number of modifications were made to Archie’s equation using shale volume (among

other parameters) to account for those effects. As our understanding of geological processes matured, it became understood that *shale* and *clay* are different and that shaly sands are usually not just sands with shales mixed in but sands that contain clays. These clays could be very different from the clays present in the shales near those sands of interest. Again, the literature and our interpretive techniques commonly use the terms *shale volume* and *clay volume* interchangeably. Most of the shaly sand techniques developed over the years concern themselves with shale volume, but a few, notably the Waxman-Smits and dual water methods, seek to use the electrical properties of the clays in the formations to predict an accurate water saturation.

Beginning in the late 1960s, the work of Waxman and Smits (1968) and Waxman and Thomas (1974) helped to better understand the physical causes of the responses of logging measurements to shaly sands and to develop interpretive models to better approximate the physical reality of formations. Clavier et al. (1977) built on the work of Waxman and his colleagues with the introduction of the dual water model for the determination of water saturation. The dual water model postulates two different types of water in a shaly formation, a immovable water layer next to the clay surfaces (bound water) and movable water that can be displaced by hydrocarbons (free water). This technique, while more complex in its use, continues to gain popularity because of its closer approximation to the responses of shaly sands in a wide variety of conditions.

The presence of shale or clay minerals in a reservoir can cause erroneous values for water saturation and porosity derived from logs. These erroneous values are not limited to sandstones but also occur in limestones and dolomites.

Essentially all measurements, then, are affected in some way by the presence of clays and/or shales. Hilchie (1978) notes that the most significant effect of shale in a formation is to reduce the resistivity contrast between oil or gas, and water. The net result is that if enough shale is present in a reservoir, it may be very difficult, or perhaps impossible, to determine if a zone is productive. Hilchie (1978) suggests that for shale to significantly affect log-derived water saturations, shale content must be greater than 10 to \(15\%\).

Remember that all shaly sandstone formulas reduce the water saturation value from the value that would be calculated if shale effect were ignored. However, this lowering of water saturation can be a problem in log evaluation, because, if a geologist overestimates shale content, a water-bearing zone might appear to be a hydrocarbon-bearing zone.

<!-- фрагмент: страницы PDF 140–146, строки исходного md 7289–7661 -->
<!-- page 140 -->
Log Interpretation

129


----
━━━ FORMAT 11: FLOW / PROCESS DIAGRAM ━━━
```mermaid
graph TD
    A[Look for clean zones] --> B{Classics}
    A --> C{Carbonates}
    B --> D[Look for resistivity]
    C --> E[Look for porosity]
    D -->|LOW| F[Water zone e<br>Use as baseline (wet)<br>comparison.]
    D -->|HIGH| G[Check porosity]
    E -->|LOW| H[Tight.<br>Unlikely pay.]
    E -->|HIGH| I[Check resistivity]
    F --> J[Zone of interest]
    G -->|LOW| K[Tight.<br>Unlikely pay.]
    G -->|HIGH| L[Zone of interest]
    H --> L
    I -->|LOW| M[Water zone<br>Use as baseline (wet)<br>comparison.]
    I -->|HIGH| N[Zone of interest]
    M --> L
    L --> O[Begin detailed analysis]
    N --> O
```
----
KEYWORDS: flowchart, reservoir evaluation, pay zone identification, clean zones, resistivity, porosity, baseline comparison, tight zones, detailed analysis


Figure 7.1. Flowchart for scanning logs to identify zones of interest (both pay and wet). The scanning flowchart has two paths, one for clastics and one for carbonates.

# **Clastics:**

The resistivity log is the primary reconnaissance measurement because clastics tend to consist of reservoirs surrounded by shales whose resistivities vary gradually with depth. Differences in the fluid content of the reservoirs tend to produce reservoir resistivities that stand out against the relatively constant resistivity of the surrounding shales.

# **Carbonates:**

Formation resistivities tend to vary widely with changing rock types, and commonly there are few shales against which to measure changes. In this case, the porosity log is the primary reconnaissance measurement. By first finding the porous zones, the zones with the capacity to hold fluids (of any type) can be identified.

Using this scanning technique in combination with the neutron-density quick-look technique discussed in Chapter 4 (if those logs are available) allows one to identify lithology (and sometimes fluid type) in the course of identifying the zones of interest.

¹ Zones that appear to be shales might be radioactive productive zones.
² Shaly zones might produce oil or gas even if they have low resistivity.


----
━━━ FORMAT 11: FLOW / PROCESS DIAGRAM ━━━
```mermaid
graph TD
    A[Data Source] --> B[Deep-reading resistivity (ILD, LL D)]
    A --> C[Shallow-reading resistivity (MSFL, MLL, Prox)]
    A --> D[Density]
    A --> E[Neutron]
    A --> F[Sonic]
    A --> G[Magnetic Resonance]
    A --> H[SP]
    A --> I[Gamma Ray]
    A --> J[Wellsite measurements]
    A --> K[Laboratory measurements]
    A --> L[Local knowledge]

    B -->|Ch.5| M[Ri]
    C -->|Ch.5| N[R40]
    D -->|Ch.4| O[Φ]
    E -->|Ch.7| O
    F -->|Ch.6| O
    G -->|Ch.6| P[Vshale]
    H -->|Ch.2| Q[Rw]
    I -->|Ch.5| R[Roof]
    J -->|Ch.4| S[σ]
    K -->|Ch.4| S
    L -->|Ch.4| S

    M --> T[Sw]
    N --> T
    O --> T
    P --> T
    Q --> T
    R --> T
    S --> T

    T --> U[Sw]
    T --> V[Sxo]
    T --> W[Movable hydrocarbons]
    T --> X[HW]
    T --> Y[Permeability]
    T --> Z[Reserves]
```
----
KEYWORDS: well logging, data flow, petrophysical interpretation, input parameters, output quantities, resistivity, density, neutron, sonic, magnetic resonance, SP, gamma ray, wellsite measurements, laboratory measurements, local knowledge, water saturation, movable hydrocarbons, permeability, reserves


Figure 7.2. Flowchart for interpretation.

The sources of raw data, both well logs and other well-bore information, are shown in the left column. In many cases, the information generated from that raw data (shown in the center column) is used in computations to produce the quantities of interest (shown in the right column).

The chart shows that there are several ways to calculate porosity ($\phi$) and shale volume ($V_{shale}$) from the raw data.

The chapters that explain the calculations are listed in the flowchart.
<!-- page 141 -->
130

ASQUITH AND KRYGOWSKI


Figure 7.3. Buckles plots (porosity vs. water saturation).

Because production of water in a well can affect a prospect's economics, it is important to know the bulk volume water and whether the formation is at irreducible water saturation ($S_{W\text{irr}}$).

These Buckles plots are taken from the Ordovician Red River B-zone, Beaver Creek Field, Golden Valley County, North Dakota (after Jaafar, 1980).

With $S_{W}$ and porosity plotted on linear scales, points of equal bulk volume water (BVW) plot as hyperbolic curves. A series of points plotting along a particular hyperbolic curve indicates that the bulk volume water is constant and that the formation is close to irreducible water saturation. A reservoir in that condition would not produce water. As the amount of formation water increases, the bulk volume water values become scattered from the hyperbolic curves and the formation has more water than it can hold by capillary pressure. The water saturation is no longer at, or near, irreducible, so more water is produced relative to oil.

Figure 7.3a is an example of nearly constant BVW. The formation shown produces 96% oil. Note that all the points plot between 0.04 and 0.05 BVW. The formation is very close to, or at, irreducible water saturation.

Figure 7.3b shows a well producing 68% oil. About half the points cluster around a BVW value of 0.04, but the other half have higher values of BVW, indicating moveable water.

Figure 7.3c shows a well producing no oil (all water). Note the scatter of BVW values from the hyperbolic curves, indicating that the formation is not at irreducible water saturation.
<!-- page 142 -->
Log Interpretation

131


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: True resistivity, Rt, logarithmic scale, range 0.10 to 100.00 (Ω·m).
- Y-axis: Density porosity, DPHI, logarithmic scale, range 0.01 to 1.00 (fractional porosity).
- Plot contains 5 diagonal lines (family of curves) labelled with values: 5, 10, 20, 50, 100, 200, 500, 1000 (units not specified, likely ppm or mg/L, as per standard Schlumberger CP palettes).
- Data points: 7 black dots plotted on the chart, distributed between Rt = 1.00 and 10.00, DPHI = 0.10 and 0.50.
- The curves are interpreted as lines of constant formation water salinity (or similar parameter) in a crossplot of resistivity vs. density porosity.
- The data points lie primarily along the curve labelled "100", with one point near "50" and one near "200".
> Тренд: С увеличением истинного сопротивления (Rt) плотностная пористость (DPHI) уменьшается; данные точек сосредоточены вдоль кривой, соответствующей значению 100 на семействе кривых.
KEYWORDS: DPHI, Rt, кривые постоянной солености, кроссплот, плотностная пористость, истинное сопротивление, логарифмическая шкала, интерпретация ГИС
----


Figure 7.4. Pickett plot (saturation crossplot or resistivity-porosity crossplot) illustrating water-bearing and hydrocarbon-bearing zones in a well.

Data are from the Morrow Sandstone, Cimarron County, Oklahoma (Table 7.4).

Density porosity was calculated assuming a matrix density of $2.65\mathrm{g/cm^3}$ and a fluid density of $1.0\mathrm{g/cm^3}$. The water-bearing line ($S_w = 100\%$) was drawn through the cluster of points with a slope of $-1/2$ ($m = 2$). (Because of the limited porosity range of the points and their scatter, other values of $m$ from 1.8 to 2.15 could be justified.)

The intercept of the water-bearing line at $100\%$ porosity ($\mathrm{DPHI} = 1.0$) is $a \times R_{a}$. If the intercept were not off the plot in this illustration, the value could be read directly from the plot. In cases such as this, the value for $a \times R_{a}$ can be determined from $R_{a}$ by using Equation 7.28.

$$
R _ {w} = \frac {R _ {a} \times \phi^ {m}}{a}
$$

Remember that $R_{a}$ is the resistivity in the undisturbed, water-bearing zone, and for all points on the water-bearing line $R_{i} = R_{a}$.

Procedure to calculate $R_{a}$:

For some porosity value, read the value of $R_{a}$ from the water-bearing line on the crossplot. In this case, for a porosity of $10\%$ ($\mathrm{DPHI} = 0.10$), $R_{a} = 4.6$ ohm-m.

Assume a value of tortuosity factor ($a$). In this case, $a = 1.0$.

The value of cementation exponent ($m$) is determined from the crossplot. In this case, $m = 2.0$.

By substitution in the above equation,

$$
R _ {w} = \frac {4 . 6 \times 0 . 1 0 ^ {3 . 0}}{1 . 0}
$$

$R_{w} = 0.046$ ohm-m at formation temperature

The water saturation lines are constructed on the plot from the value for $R_{a}$ and the multipliers from Table 7.2. The multipliers are for a saturation exponent ($n$) of 2.0. For each line to be plotted, multiply $R_{a}$ by the multiplier to get the $y$-intercept and draw a line from the $y$-intercept parallel to the water-bearing line. To plot the line for $50\%$ water saturation, for example, if $R_{a}$ (at $\mathrm{DPHI} = 0.10$) is 4.6 and the multiplier (from Table 7.2) is 4, the $y$-intercept for the $50\%$ water saturation line (at $\mathrm{DPHI} = 0.10$) is 18.4.

To determine the water saturation of the anomalous points (with more accuracy than estimating the values from the crossplot), the following equation can be used:

$$
S _ {w} = \left(\frac {R _ {a}}{R _ {r}}\right) ^ {\frac {1}{n}}
$$

In this case, the value for $R_{a}$ is the value at the water-bearing line at the same porosity as the point of interest. For the two points of interest (both having the same porosity), $R_{a} = 0.80$ ohm-m. For the point who's resistivity is 40 ohm-m, the saturation is found by:

$$
S _ {w} = \left(\frac {0 . 8}{4 0}\right) ^ {\frac {1}{2 . 0}}
$$

$$
S _ {w} = 0. 1 4
$$

For comparison interpretation, Figure 7.7 is a Hingle plot with the same data shown.
<!-- page 143 -->
132

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения пористости по удельной проводимости и удельному сопротивлению.

Ось абсцисс (горизонтальная): Пористость, φ — линейная шкала, диапазон от 0 до 1 (не указано, но по структуре палетки — доля, безразмерная).

Ось ординат (левая вертикальная): Проводимость, Ca — логарифмическая шкала, диапазон от 0 до 2000 (mmho/m), с делениями: 0, 5, 10, 20, 50, 100, 200, 500, 1000, 1500, 2000.

Ось ординат (правая вертикальная): Удельное сопротивление, R — логарифмическая шкала, диапазон от 0.5 до ∞ (Ω·m), с делениями: 0.5, 0.6, 0.7, 0.8, 1, 1.2, 1.5, 2, 2.5, 3, 5, 10, 15, 20, 50, 100, 200, 500, 1000, ∞.

Семейство кривых: не указано, но по структуре — это палетка для определения пористости φ по Ca и R, предположительно для различных значений параметра водонасыщенности (например, m, n, a) или для различных типов пород. На палетке нет явно промаркированных кривых, но присутствуют горизонтальные линии, соответствующие значениям φ, и вертикальные линии, соответствующие значениям Ca и R.

Процедура чтения: по оси ординат (Ca или R) найти значение, затем по горизонтальной линии, проходящей через это значение, определить пористость φ на оси абсцисс. Поскольку Ca и R связаны обратно (Ca = 1/R), палетка представляет собой одну и ту же зависимость, отображённую с двух сторон.

Ориентировочные точки (для крайних кривых, если бы они были параметризованы):
- При φ = 0.1 (10%) и Ca = 100 mmho/m → R = 0.01 Ω·m (не на шкале, но по обратной связи).
- При φ = 0.1 и Ca = 10 mmho/m → R = 0.1 Ω·m.
- При φ = 0.1 и Ca = 1 mmho/m → R = 1 Ω·m.
- При φ = 0.1 и Ca = 0.1 mmho/m → R = 10 Ω·m.

Примечание: палетка не содержит явных параметров (например, m, n, a), но её структура соответствует стандартным палеткам для определения пористости по удельной проводимости (или сопротивлению) в предположении постоянных параметров Арчи.

KEYWORDS: палетка, удельная проводимость, удельное сопротивление, пористость, логарифмическая шкала, интерпретация ГИС, Арчи, Ca, R, φ
----


Figure 7.5. Hingle plot (saturation crossplot or resistivity-porosity crossplot) generally used for sandstones. (Western Atlas International, Inc., 1995, Chart 7-79)
The y-axis is constructed with tortuosity factor (a) = 1.0 and cementation exponent (m) = 2.0.
<!-- page 144 -->
Log Interpretation

133


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения удельного сопротивления и проводимости.

Ось абсцисс (горизонтальная): не указана, но предполагается, что это ось для ввода параметра (например, пористости, глинистости или другого параметра, используемого в интерпретации).

Ось ординат (вертикальная, левая): Conductivity, C, (mmho/m) — логарифмическая шкала, диапазон от 0 до 100, с делениями: 0, 0.5, 1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100.

Ось ординат (вертикальная, правая): Resistivity, R, (Ω • m) — логарифмическая шкала, диапазон от ∞ до 10, с делениями: ∞, 20,000, 5000, 1000, 500, 200, 100, 50, 25, 20, 15, 10.

Семейство кривых: не указано, но предполагается, что это семейство кривых, соответствующих различным значениям глинистости, пористости или другого параметра, используемого для интерпретации. В данном изображении кривые не нанесены — показана только сетка координат.

Процедура чтения: по оси абсцисс задаётся значение параметра (например, пористость), по соответствующей кривой (для заданной глинистости) снимается значение проводимости (C) по левой оси или удельного сопротивления (R) по правой оси.

Анкерные точки (ориентировочно, для крайних кривых, если бы они были):
- При C = 1 mmho/m → R = 1000 Ω·m
- При C = 10 mmho/m → R = 100 Ω·m
- При C = 100 mmho/m → R = 10 Ω·m

Примечание: в данном изображении отсутствуют кривые, поэтому палетка не может быть использована для интерпретации без дополнительных данных.

KEYWORDS: палетка, удельное сопротивление, проводимость, логарифмическая шкала, интерпретация, ГИС, C, R, Ω·m, mmho/m
----


Figure 7.6. Hingle plot (saturation crossplot or resistivity-porosity crossplot) generally used for carbonates. (Western Atlas International, Inc., 1995, Chart 7-80) The y-axis is constructed with tortuosity factor (a) = 0.62 and cementation exponent (m) = 2.15
<!-- page 145 -->
134

ASQUITH AND KRYGOWSKI

Figure 7.7. Hingle plot (saturation crossplot or resistivity-porosity crossplot) illustrating water-bearing and hydrocarbon-bearing zones in a well. Data are from the Morrow Sandstone, Cimarron County, Oklahoma (Table 7.4).

The Hingle grid using a = 1.0 and m = 2.0 was chosen as the common parameters for sandstones.

The x-axis has been scaled in bulk density, and the points plotted accordingly. The water-bearing line drawn through the cluster of points intersects the y-axis at 2.65 g/cm³, the matrix-density value for the formation. (Given the limited porosity range and the scatter of those points, other values for matrix density could also be justified.)

R_w is determined using Equation 7.28:

$$R_w = \frac{R_c \times \phi^m}{a}$$

For some porosity value, read the value of R_a from the water-bearing line on the crossplot. In this case, for a porosity of 10% (bulk density = 2.485 g/cm³), R_a = 4.1 ohm-m.

The values of tortuosity factor (a) and cementation exponent (m) were assumed by choice of the particular crossplot grid.

By substitution in the above equation,

$$R_w = \frac{4.1 \times 0.10^{2.0}}{1.0}$$

R_w = 0.041 ohm-m at formation temperature

The water saturation lines are constructed on the plot from the value for R_a and the multipliers from Table 7.2. The multipliers are for a saturation exponent (n) of 2.0.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of bulk density versus conductivity (or resistivity) with water saturation contours.

Left Y-axis: Conductivity, C, in mmho/m, linear scale, range 0 to 2000.
Right Y-axis: Resistivity, R, in (Ω·m), linear scale, range 0.5 to 500 (logarithmic scale implied by tick marks: 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500).
X-axis: Bulk density, in g/cm³, linear scale, range 2.25 to 2.65.

The plot contains a family of curves representing constant water saturation (Sw), labelled: 30, 50, 70, 100. These curves are straight lines radiating from the origin (0,0) in the lower-left corner. The Sw=100 curve is the steepest, Sw=30 is the shallowest.

Data points are shown as black filled circles. There are 10 data points plotted. Their approximate coordinates (Bulk density, Conductivity) are:
- (2.35, 50)
- (2.35, 100)
- (2.38, 200)
- (2.40, 300)
- (2.42, 400)
- (2.44, 500)
- (2.46, 700)
- (2.48, 1000)
- (2.50, 1200)
- (2.52, 1500)

The data points lie approximately along the Sw=50 curve, suggesting a water saturation of around 50% for these samples.

The plot is a standard interpretation chart used in petrophysics to estimate water saturation from bulk density and resistivity (or conductivity) measurements.

> Тренд: С увеличением плотности породы (с 2.25 до 2.65 г/см³) проводимость уменьшается, а удельное сопротивление увеличивается. Кривые постоянной водонасыщенности (Sw) идут от начала координат, и данные точки лежат вблизи кривой Sw=50, что указывает на среднюю водонасыщенность.

KEYWORDS: проводимость, удельное сопротивление, плотность, водонасыщенность, Sw, кривые постоянной водонасыщенности, петрофизика, интерпретация, керн, ГИС
----


For each line to be plotted, multiply R_a by the multiplier and plot that line so that it intersects the water-bearing line at infinite resistivity. In this example, R_a (at bulk density = 2.485 g/cm³) is 4.1. The intercept for the 50% water-saturation line (at bulk density = 2.485 g/cm³) is 16.4.

To determine the water saturation of the anomalous points (with more accuracy than estimating the values from the crossplot), the following equation can be used:

$$S_w = \left(\frac{R_a}{R_s}\right)^{\frac{1}{n}}$$

In this case, the value for R_a is the value at the water-bearing line at the same porosity as the point of interest. For the two points of interest (both having the same porosity), R_a = 0.83 ohm-m. For the point who's resistivity is 40 ohm-m, the saturation is found by:

$$S_w = \left(\frac{0.83}{40}\right)^{\frac{1}{2.0}}$$

$$S_w = 0.144$$

For comparison of interpretation, Figure 7.4 is a Pickett plot with the same data shown.
<!-- page 146 -->
Log Interpretation

135


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения насыщенности воды в зоне перехода выше водоносного горизонта (S_w, water saturation above transition zone) в зависимости от пористости (φ, porosity) и проницаемости (k, permeability).

Ось абсцисс (горизонтальная): φ, porosity (p.u.), линейная шкала, диапазон 0–40.
Ось ординат (вертикальная): S_w, water saturation above transition zone (%), линейная шкала, диапазон 0–60.

Семейство кривых: параметр — проницаемость k, permeability (md), с подписями: 0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.2, 0.5, 1.0, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000.

Процедура чтения: по оси абсцисс задаётся пористость φ, по кривой, соответствующей заданной проницаемости k, снимается значение S_w на оси ординат.

Анкерные точки (ориентировочно):
- Для k = 0.01 md: при φ = 5 p.u. → S_w ≈ 50%; при φ = 10 p.u. → S_w ≈ 35%
- Для k = 100 md: при φ = 15 p.u. → S_w ≈ 20%; при φ = 25 p.u. → S_w ≈ 10%
- Для k = 5000 md: при φ = 30 p.u. → S_w ≈ 10%; при φ = 35 p.u. → S_w ≈ 8%

> Тренд: с увеличением проницаемости при фиксированной пористости насыщенность воды в зоне перехода уменьшается; при фиксированной проницаемости с ростом пористости S_w снижается.

KEYWORDS: палетка, насыщенность воды, пористость, проницаемость, зона перехода, ВНК, интерпретация ГИС, S_w, k, φ, номограмма, петрофизика


Figure 7.8. Chart of porosity ($\phi$) versus irreducible water saturation ($S_{wi}$ in) for estimating permeability and determining bulk volume water. (Schlumberger, 1998, Chart K-3)

Given: Porosity ($\phi$) = 0.25 (= 25 porosity units, p.u.) and irreducible water saturation ($S_{wi}$ in) = 40% for an oil-bearing sandstone. The chart is constructed with the assumption of a medium-gravity oil.

Procedure:

1. Find porosity ($\phi$ = 25 p.u.) on the bottom horizontal scale, and find irreducible water saturation ($S_{wi}$ in = 40%) on the left vertical scale.

Note that irreducible water saturation is labeled $S_{wi}$ on this chart.

Follow the two values into the chart to the point where they intersect.

2. The heavy curve on which this point falls represents permeability. In this case, permeability, K = 130 md.
3. The light hyperbolic curves ($C = S_{wi} \times \phi$) represent lines of equal value for bulk volume water. In this example, the bulk volume water equals 0.10 (BVW = 0.10).

Note: It is important to remember that this chart is only valid for estimating permeability (K) in zones at irreducible water saturation ($S_{wi}$ in).

Zones at irreducible water saturation have bulk volume water values that are fairly constant. On the chart, data points from different intervals in a zone at irreducible saturation plot in a coherent pattern, on or parallel to one of the hyperbolic curves. Data points from zones not at $S_{wi}$ in scatter from this pattern.