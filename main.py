import random
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

import streamlit as st
st.title("Science Bowl Question Generator")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

science_bowl_topics = {
    "Physics": 0.25,
    "Chemistry": 0.25,
    "Biology": 0.25,
    "Math": 0.25,
    "Energy": 0,
}

subtopics = {
    "Math": ["Triangles", "Quadrilaterals", "Coordinate Plane", "Area and Perimeter", "Volume and surface area", "Pythagorean Theorem", "Congruence", "Similarity", "Circles", "Composite and Inverse Functions", "Complex numbers", "Rational functions", "Conic secctions", "Vectors", "Matrices", "Series", "Polynomial multiplication/division/arithmetic", "Logarithms", "Exponential models", "Trigonometric identities", "Trigonometric equations", "Law of cosines/sines", "Unit circle", "Limits and Continuity", "Derivatives", "Derivative Tests", "Integrals", "Differential equations", "Polar coordinates"],
    "Chemistry": ["Atoms, Molecules, Ions", "Stoichiometry", "Organic and Biological Molecules", "Types of Chemical Reactions and Solution Stoichiometry", "Gases", "Thermochemistry", "Atomic Structure and Periodicity", "Bonding: General Concepts", "Covalent Bonding: Orbitals", "Liquids and Solids", "Properties of Solutions", "Chemical Kinetics", "Chemical Equilibrium", "Acids and Bases", "Acid-Base Equilibria", "Solubility and Complex Ion Equilibria", "Spontaneity, Entropy, and Free Energy"],
    "Biology": ["The Chemical Context of Life", "Water and Life", "Carbon and the Molecular Diversity of Life", "The Structure and Function of Large Biological Molecules", "A Tour of the Cell", "Membrane Structure and Function", "An Introduction to Metabolism", "Cellular Respiration and Fermentation", "Photosynthesis", "Cell Communication", "The Cell Cycle", "Meiosis and Sexual Life Cycles", "Mendel and the Gene Idea"],
    "Physics": ["Motion Along a Straight Line", "Vectors", "Motion in Two and Three Dimensions", "Force and Motion—I", "Force and Motion—II", "Kinetic Energy and Work", "Potential Energy and Conservation of Energy", "Center of Mass and Linear Momentum", "Rotation", "Rolling, Torque, and Angular Momentum", "Equilibrium and Elasticity", "Gravitation", "Fluids", "Oscillations", "Waves-I", "Waves-II", "Temperature, Heat, and the First Law of Thermodynamics", "The Kinetic Theory of Gases", "Entropy and the Second Law of Thermodynamics", "Coulomb’s Law", "Electric Fields", "Gauss's Law", "Electric Potential", "Capacitance"]
}

question_styles = {
    "Physics": ["Short Answer Direct Term", "Short Answer Numerical", "Multiple Choice Direct Term", "Multiple Choice Numerical", "Multiple Choice Analytical", "Short Answer Numbered Identification"],
    "Biology": ["Short Answer Direct Term", "Multiple Choice Direct Term", "Multiple Choice Analytical", "Short Answer Numbered Identification"],
    "Chemistry": ["Short Answer Direct Term", "Short Answer Numerical", "Multiple Choice Direct Term", "Multiple Choice Numerical", "Multiple Choice Analytical", "Short Answer Numbered Identification"]
}

question_styles_examples = {
    "Physics": [" Physics – Short Answer What semiconductor device was instrumental in replacing vacuum tubes as the basic logical component in digital electronics? ANSWER: TRANSISTOR", " Physics – Short Answer A remote control car drops from a cliff and travels 19.6 meters before hitting the ground. How long, in seconds, did it spend in the air? ANSWER: 2", "Energy – Multiple Choice Fermi National Accelerator scientists are looking for physics beyond the Standard Model in the form of decay pathways that do not conserve lepton flavor. Which of the following particles has already been observed violating this conservation principle? W) Electrons X) Neutrinos Y) Protons Z) Bosons ANSWER: X) NEUTRINOS", " Physics – Multiple Choice Kate is tuning her cello's A string by producing an A note on a string that is already tuned and comparing the sounds. Which of the following beat frequencies, in hertz, would indicate that the strings are closest to having the same pitch? W) 2 X) 100 Y) 440 Z) 880 ANSWER: W) 2", " Physics – Multiple Choice An asteroid with linear momentum is gravitationally captured by a planet. Which of the following best explains where the linear momentum of the asteroid went? W) Converted into angular momentum X) Conserved in the asteroid's orbital velocity Y) Dissipated by frictional forces Z) Translating the planet-asteroid system ANSWER: Z) TRANSLATING THE PLANET-ASTEROID SYSTEM", " Physics – Short Answer Identify all of the following three statements that are true of free- fall: 1) Apparent weightlessness is the sensation that occurs when the gravitational force is negated by air friction; 2) Satellites orbiting the earth are in near free-fall; 3) Objects free-falling on Earth all reach terminal velocity. ANSWER: 2"],
    "Biology": [" Biology – Short Answer Atherosclerotic [athero-sklair-AW-tic] plaques are composed of what lipid that is stored in LDL and HDL particles? ANSWER: CHOLESTEROL", " Biology – Multiple Choice In which of the following organ systems do the tonsils primarily function? W) Lymphatic X) Digestive Y) Respiratory Z) Integumentary [in-TEG-you-MEN-tary] ANSWER: W) LYMPHATIC ", "Biology – Multiple Choice A population of actively dividing cells contains, on average, 30 femtograms of DNA per cell. After some period of time, you make another measurement and observe that the cells now have 60 femtograms of DNA per cell. Which of the following is the most reasonable conclusion to make about these cells? W) They are going to perform meiosis [my-OH-sis] X) They are going to perform mitosis Y) S phase has occurred Z) They are in G1 phase ANSWER: Y) S PHASE HAS OCCURRED ", "Biology – Short Answer Identify all of the following four cell types that are considered white blood cells: 1) T cells; 2) Erythrocytes; 3) Thrombocytes; 4) Neutrophils. ANSWER: 1, 4 "],
    "Chemistry": [" Chemistry – Short Answer What is the name of the aldehyde [AL-deh-hide] with only a single carbon atom? ANSWER: FORMALDEHYDE (ACCEPT: METHANAL) ", "Chemistry – Short Answer Suppose that at a certain temperature, one mole of chlorine gas and one mole of PCl3 gas are placed in a 1-liter container, and then equilibrate to form 0.2 moles of PCl5 gas. What is the K-sub-C value for the gas-phase reaction PCl3 + Cl2 yields PCl5 at this temperature? ANSWER: 5/16 (ACCEPT: 0.3125)", "Chemistry – Multiple Choice Which of the following alkali metals has the most negative standard reduction potential? W) Sodium X) Cesium Y) Rubidium [roo-BID-ee-um] Z) Potassium ANSWER: X) CESIUM", "Chemistry – Multiple Choice A balloon is inflated with 10 grams of helium. Under the same conditions, a second balloon is inflated to the same volume with nitrogen. To the nearest gram, what is the mass of nitrogen in the second balloon? W) 40 X) 50 Y) 60 Z) 70 ANSWER: Z) 70 ", " Chemistry – Multiple Choice Kevin performs a titration [tie-TRAY-shun] using sodium hydroxide as the titrant. He finds that the pH at the equivalence point is above 7. What does this imply about the analyte? W) It is a strong acid X) It is a weak acid Y) It is a strong base Z) It is a weak base ANSWER: X) IT IS A WEAK ACID", "Chemistry – Short Answer Identify all of the following four molecules that are linear: 1) Carbon dioxide; 2) Selenium [sih-LEE-nee-um] dioxide; 3) Beryllium dichloride; 4) Xenon [ZEE-non] difluoride. ANSWER: 1, 3, AND 4 "]
}

question_style_explanations = {
    "Short Answer Direct Term": "This question must be short answer and have a specific term as an answer.",
    "Short Answer Numerical": "This question must be short answer and have a number as an answer.",
    "Multiple Choice Direct Term": "This question must be multiple-choice and have specific terms as answer choices.",
    "Multiple Choice Numerical": "This question must be multiple-choice and have numbers as answer choices.",
    "Multiple Choice Analytical": "This question must be multiple-choice and require critical thinking, involving a long question with lengthy, sentence long answer choices.",
    "Short Answer Numbered Identification": "This question must be short answer and have three answer choices numbered with 1,2, and 3, and the question must ask to identify all of the following choices that are true."
}

def select_topic():
    category = random.choices(list(science_bowl_topics.keys()), weights=list(science_bowl_topics.values()))[0]
    if(category=="Energy"):
        topic = ""
    else:
        topic = random.choice(subtopics[category])
    return category, topic
    
import numpy as np

phys_text = [
    '''
Position The position x of a particle on an x axis locates the par- ticle with respect to the origin, or zero point, of the axis. The position is either positive or negative, according to which side of the origin the particle is on, or zero if the particle is at the origin. The positive direction on an axis is the direction of increasing positive numbers; the opposite direction is the negative direction on the axis.
Displacement The displacement Ax of a particle is the change in its position:
Ax = x2-x1.
(2-1) Displacement is a vector quantity. It is positive if the particle has moved in the positive direction of the x axis and negative if the particle has moved in the negative direction.
Average Velocity When a particle has moved from position x to position x during a time interval At = t2- t1, its average velocity during that interval is
Vavg
Ax At
Xx2x1 42-4
(2-2)
The algebraic sign of Vavg indicates the direction of motion (Vavg is a vector quantity). Average velocity does not depend on the actual distance a particle moves, but instead depends on its original and final positions.
On a graph of x versus t, the average velocity for a time interval At is the slope of the straight line connecting the points on the curve that represent the two ends of the interval.
Average Speed The average speed s, of a particle during a time interval At depends on the total distance the particle moves in that time interval:
Savg
total distance Δε
(2-3)
Instantaneous Velocity The instantaneous velocity (or sim- ply velocity) v of a moving particle is
QUESTIONS
31
and the second time derivative of position x(t):
dv
d2x
dt
dt2
(2-8,2-9)
On a graph of v versus t, the acceleration a at any time t is the slope of the curve at the point that represents t.
Ax v = lim Ar 0 At
dx dt'
Constant Acceleration The five equations in Table 2-1 describe the motion of a particle with constant acceleration:
(2-4)
v = vo + at,
(2-11)
x = x0 = vot + at2,
(2-15)
v2 = vz + 2a(x − xo),
-
(2-16)
x − x0 = {(Vo+v)t,
(2-17)
x = x0 = vt at2.
-
(2-18)
where Ax and At are defined by Eq. 2-2. The instantaneous velocity (at a particular time) may be found as the slope (at that particular time) of the graph of x versus t. Speed is the magnitude of instanta- neous velocity.
Average Acceleration Average acceleration is the ratio of a change in velocity Av to the time interval At in which the change occurs:
a avg
Av Δε
The algebraic sign indicates the direction of aavg.
(2-7)
Instantaneous Acceleration Instantaneous acceleration (or simply acceleration) a is the first time derivative of velocity v(t)
These are not valid when the acceleration is not constant.
Free-Fall Acceleration An important example of straight- line motion with constant acceleration is that of an object rising or falling freely near Earth's surface. The constant acceleration equa- tions describe this motion, but we make two changes in notation: (1) we refer the motion to the vertical y axis with +y vertically up; (2) we replace a with -g, where g is the magnitude of the free-fall acceleration. Near Earth's surface, g = 9.8 m/s2 (= 32 ft/s2).
    ''',

    '''
Review & Summary
Scalars and Vectors Scalars, such as temperature, have magni- tude only. They are specified by a number with a unit (10°C) and obey the rules of arithmetic and ordinary algebra. Vectors, such as displacement, have both magnitude and direction (5 m, north) and obey the rules of vector algebra.
Adding Vectors Geometrically Two vectors a and b may be added geometrically by drawing them to a common scale and placing them head to tail. The vector connecting the tail of the first to the head of the second is the vector sum 3. To subtract from a, reverse the direction of b to get -b; then add -b to a. Vector addition is commutative
and obeys the associative law
(a + b) + ¿ = a + (b + c).
(3-2)
(3-3)
Components of a Vector The (scalar) components a, and a, of any two-dimensional vector a along the coordinate axes are found by dropping perpendicular lines from the ends of a onto the coor- dinate axes. The components are given by
a = a cos @ and a1, = a sin 0,
(3-5)
where is the angle between the positive direction of the x axis and the direction of a. The algebraic sign of a component indi- cates its direction along the associated axis. Given its compo- nents, we can find the magnitude and orientation (direction) of the vector a by using
a = √a + a2 and tan 0 =
ay ax
(3-6)
Unit-Vector Notation Unit vectors i, j, and â have magnitudes of unity and are directed in the positive directions of the x, y, and z axes, respectively, in a right-handed coordinate system (as defined by the vector products of the unit vectors). We can write a vector a in terms of unit vectors as
a = ai +a,j+ak,
(3-7)
in which ai, a,j, and aşk are the vector components of a and ax, ay, and a, are its scalar components.
Adding Vectors in Component Form To add vectors in com- ponent form, we use the rules
ry=a, + by
rab (3-10 to 3-12)
rx = ax + bx Here a and b are the vectors to be added, and 7 is the vector sum. Note that we add components axis by axis. We can then express the sum in unit-vector notation or magnitude-angle notation.
Product of a Scalar and a Vector The product of a scalar s and a vector v is a new vector whose magnitude is sv and whose direc- tion is the same as that of v if s is positive, and opposite that of v if s is negative. (The negative sign reverses the vector.) To divide v by s, multiply by 1/s.
The Scalar Product The scalar (or dot) product of two vectors a and b is written a·b and is the scalar quantity given by
a. b = ab cos p,
(3-20)
in which is the angle between the directions of a and B. A scalar product is the product of the magnitude of one vector and the scalar component of the second vector along the direction of the first vector. Note that a·bba, which means that the scalar product obeys the commutative law.
In unit-vector notation,
ab(a+a+a,k)·(b,i+b,j +b,k),
which may be expanded according to the distributive law.
(3-22)
The Vector Product The vector (or cross) product of two vectors a and b is written a× б and is a vector whose magnitude c is given by (3-24)
c = ab sin o,
in which is the smaller of the angles between the directions of a and . The direction of 2 is perpendicular to the plane defined by a and b and is given by a right-hand rule, as shown in Fig. 3-19. Note that a × b = -(b×ā), which means that the vec- tor product does not obey the commutative law. In unit-vector notation,
ä×b (a,i+a+a,k) × (b,i +b‚j +b ̧k), (3-26) which we may expand with the distributive law.
    ''',

    '''
Review & Summary
Position Vector The location of a particle relative to the ori- gin of a coordinate system is given by a position vector 7, which in unit-vector notation is
7 = xî + yĵ + zk.
(4-1)
Here xỉ, y, and zk are the vector components of position vector 7, and x, y, and z are its scalar components (as well as the coordinates of the particle). A position vector is described either by a magni- tude and one or two angles for orientation, or by its vector or scalar components.
Displacement If a particle moves so that its position vector changes from 71 to 72, the particle's displacement A is
As At in Eq. 4-8 is shrunk to 0, avg reaches a limit called either the velocity or the instantaneous velocity v:
dr dt'
which can be rewritten in unit-vector notation as
(4-10)
(4-11)
where v1 = dx/dt, v, = dy/dt, and v2 = dz/dt. The instantaneous velocity of a particle is always directed along the tangent to the particle's path at the particle's position.
Average Acceleration and Instantaneous Acceleration If a particle's velocity changes from v1 to v2 in time interval At, its average acceleration during At is V2V1 AV
A7 = 72-71.
(4-2)
The displacement can also be written as
a ave
(4-15)
Δε
Δε
A7 = (x2 − x1)î + (y1⁄2 − y1)Î + (Z2 − Z1)Ê = Axi + Ayj + Azk.
(4-3) (4-4)
As At in Eq. 4-15 is shrunk to 0, avg reaches a limiting value called either the acceleration or the instantaneous acceleration a:
Average Velocity and Instantaneous Velocity If a parti- cle undergoes a displacement A7 in time interval At, its average ve- locity Vavg for that time interval is
ā
dv dt
(4-16)
In unit-vector notation,
Vave
ΔΡ Δε
(4-8)
a = a,î + a‚j + a2k, where a = dv/dt, a, = dv/dt, and a2 = dv2/dt.
(4-17)
82
CHAPTER 4 MOTION IN TWO AND THREE DIMENSIONS
Projectile Motion Projectile motion is the motion of a particle that is launched with an initial velocity Vo. During its flight, the par- ticle's horizontal acceleration is zero and its vertical acceleration is the free-fall acceleration -g. (Upward is taken to be a positive di- rection.) If v is expressed as a magnitude (the speed vo) and an an- gle (measured from the horizontal), the particle's equations of motion along the horizontal x axis and vertical y axis are
x-xo (Vo cos 0)t,
yyo
(vo sin 00)t - gt2,
(4-21)
(4-22)
(4-23)
(4-24)
Uniform Circular Motion If a particle travels along a circle or circular arc of radius r at constant speed v, it is said to be in uniform circular motion and has an acceleration a of constant magnitude
(4-34)
The direction of a is toward the center of the circle or circular arc, and a is said to be centripetal. The time for the particle to complete a circle is
2πr
T =
ν
(4-35)
Vyvo sin - gt,
v = (vo sin 66)2-2g(y-yo).
The trajectory (path) of a particle in projectile motion is parabolic and is given by
y = (tan 0)x
gx2 2(vo cos 80)2
(4-25)
if x and yo of Eqs. 4-21 to 4-24 are zero. The particle's horizontal range R, which is the horizontal distance from the launch point to the point at which the particle returns to the launch height, is
R =
v g
sin 200-
(4-26)
T is called the period of revolution, or simply the period, of the motion.
Relative Motion When two frames of reference A and B are moving relative to each other at constant velocity, the velocity of a par- ticle P as measured by an observer in frame A usually differs from that measured from frame B. The two measured velocities are related by
VPA = VPB + VBA
(4-44)
where VBA is the velocity of B with respect to A. Both observers measure the same acceleration for the particle:
aPA= a PB.
(4-45)
    ''',

    '''


Review & Summary
Newtonian Mechanics The velocity of an object can change (the object can accelerate) when the object is acted on by one or more forces (pushes or pulls) from other objects. Newtonian me- chanics relates accelerations and forces.
Force Forces are vector quantities. Their magnitudes are de- fined in terms of the acceleration they would give the standard kilogram. A force that accelerates that standard body by exactly 1 m/s2 is defined to have a magnitude of 1 N. The direction of a force is the direction of the acceleration it causes. Forces are com- bined according to the rules of vector algebra. The net force on a body is the vector sum of all the forces acting on the body.
Newton's First Law If there is no net force on a body, the body remains at rest if it is initially at rest or moves in a straight line at constant speed if it is in motion.
Inertial Reference Frames Reference frames in which Newtonian mechanics holds are called inertial reference frames or inertial frames. Reference frames in which Newtonian mechanics does not hold are called noninertial reference frames or noniner- tial frames.
Mass The mass of a body is the characteristic of that body that relates the body's acceleration to the net force causing the acceler- ation. Masses are scalar quantities.
Newton's Second Law The net force Fnet on a body with mass m is related to the body's acceleration a by
Fe-ma,
which may be written in the component versions
(5-1)
Fnet, x = max Fnet, y = may
and
Fnet, z
= ma2.
(5-2)
The second law indicates that in SI units
A free-body diagram is a stripped-down diagram in which only one body is considered. That body is represented by either a sketch or a dot. The external forces on the body are drawn, and a coordinate system is superimposed, oriented so as to simplify the solution.
Some Particular Forces A gravitational force Fg on a body is a pull by another body. In most situations in this book, the other body is Earth or some other astronomical body. For Earth, the force is directed down toward the ground, which is assumed to be an inertial frame. With that assumption, the magnitude of Fis
F = mg,
(5-8)
where m is the body's mass and g is the magnitude of the free-fall acceleration.
The weight W of a body is the magnitude of the upward force needed to balance the gravitational force on the body. A body's weight is related to the body's mass by
W = mg.
(5-12)
A normal force F is the force on a body from a surface against which the body presses. The normal force is always perpen- dicular to the surface.
A frictional force ƒ is the force on a body when the body slides or attempts to slide along a surface. The force is always par- allel to the surface and directed so as to oppose the sliding. On a frictionless surface, the frictional force is negligible.
When a cord is under tension, each end of the cord pulls on a body. The pull is directed along the cord, away from the point of at- tachment to the body. For a massless cord (a cord with negligible mass), the pulls at both ends of the cord have the same magnitude T, even if the cord runs around a massless, frictionless pulley (a pul- ley with negligible mass and negligible friction on its axle to op- pose its rotation).
Newton's Third Law If a force FBC acts on body B due to body C, then there is a force FCB on body C due to body B:
1 N = 1 kg. m/s2.
(5-3)
Fac=-FCB

    ''',

    '''


Review & Summary
Friction When a force F tends to slide a body along a surface, a frictional force from the surface acts on the body. The frictional force is parallel to the surface and directed so as to oppose the sliding. It is due to bonding between the atoms on the body and the atoms on the surface, an effect called cold-welding.
If the body does not slide, the frictional force is a static frictional force f. If there is sliding, the frictional force is a kinetic frictional force fk.
1. If a body does not move, the static frictional force F, and the component of F parallel to the surface are equal in magnitude, and F, is directed opposite that component. If the component increases, f, also increases.
2. The magnitude of F, has a maximum value fs,max given by
f=MFN
(6-1)
where μ, is the coefficient of static friction and F is the magni- tude of the normal force. If the component of F parallel to the surface exceeds fs,max, the static friction is overwhelmed and the body slides on the surface.
3. If the body begins to slide on the surface, the magnitude of the frictional force rapidly decreases to a constant value f given by
fx=μ1FN
where μ is the coefficient of kinetic friction.
(6-2)
Drag Force When there is relative motion between air (or some other fluid) and a body, the body experiences a drag force Ď that opposes the relative motion and points in the direction in which the fluid flows relative to the body. The magnitude of Ď is
related to the relative speed v by an experimentally determined drag coefficient C according to
D - CpAv2,
(6-14)
where p is the fluid density (mass per unit volume) and A is the effective cross-sectional area of the body (the area of a cross sec- tion taken perpendicular to the relative velocity v).
Terminal Speed When a blunt object has fallen far enough through air, the magnitudes of the drag force Ď and the gravita- tional force Fg on the body become equal. The body then falls at a constant terminal speed v, given by
2F
g
V1
CpA
(6-16)
Uniform Circular Motion If a particle moves in a circle or a circular arc of radius R at constant speed v, the particle is said to be in uniform circular motion. It then has a centripetal acceleration a with magnitude given by
v2 R
(6-17)
This acceleration is due to a net centripetal force on the particle, with magnitude given by
F =
mv2 R
(6-18)
where m is the particle's mass. The vector quantities a and Fare directed toward the center of curvature of the particle's path. A particle can move in circular motion only if a net centripetal force acts on it.

    ''',

    '''


Review & Summary
Kinetic Energy The kinetic energy K associated with the mo- tion of a particle of mass m and speed v, where v is well below the speed of light, is
K = mv2 (kinetic energy).
(7-1)
Work Work W is energy transferred to or from an object via a force acting on the object. Energy transferred to the object is posi- tive work, and from the object, negative work.
Work Done by a Constant Force The work done on a par- ticle by a constant force F during displacement & is
(work, constant force),
(7-7,7-8)
W = Fd cos = F⋅d in which is the constant angle between the directions of F and d. Only the component of F that is along the displacement & can do work on the object. When two or more forces act on an object, their net work is the sum of the individual works done by the forces, which is also equal to the work that would be done on the object by the net force Fnet of those forces.
Work and Kinetic Energy For a particle, a change AK in the kinetic energy equals the net work W done on the particle:
AK = K1- K1 = W (work-kinetic energy theorem), (7-10)
in which K, is the initial kinetic energy of the particle and K, is the ki- netic energy after the work is done. Equation 7-10 rearranged gives us (7-11)
K1 = K1 + W.
Work Done by the Gravitational Force The work W done by the gravitational force Fon a particle-like object of mass m as the object moves through a displacement & is given by mgd cos 6, (7-12)
W
in which is the angle between Fg and d.
g
Work Done in Lifting and Lowering an Object The work W done by an applied force as a particle-like object is either lifted or lowered is related to the work Wg done by the gravitational force and the change AK in the object's kinetic energy by
AK = K1-K;= Wa + Wg.
If K1 = K1, then Eq. 7-15 reduces to
Wa=-Wg
(7-15)
(7-16)
which tells us that the applied force transfers as much energy to the object as the gravitational force transfers from it.
QUESTIONS
169
Spring Force The force F, from a spring is
F = -kd
(Hooke's law), (7-20) where a is the displacement of the spring's free end from its posi- tion when the spring is in its relaxed state (neither compressed nor extended), and k is the spring constant (a measure of the spring's stiffness). If an x axis lies along the spring, with the origin at the lo- cation of the spring's free end when the spring is in its relaxed state, Eq. 7-20 can be written as
F-kx
(Hooke's law).
(7-21)
A spring force is thus a variable force: It varies with the displacement of the spring's free end.
Work Done by a Spring Force If an object is attached to the spring's free end, the work W, done on the object by the spring force when the object is moved from an initial position x¡ to a final position x, is
W1 =kx} - kx}.
If x = 0 and x = x, then Eq. 7-25 becomes
W1 = -kx2.
(7-25)
(7-26)
Work Done by a Variable Force When the force F on a particle- like object depends on the position of the object, the work done by F on the object while the object moves from an initial position r, with co- ordinates (x, y, z) to a final position r, with coordinates (xf, yf, Zf)
must be found by integrating the force. If we assume that component F, may depend on x but not on y or z, component F, may depend on y but not on x or z, and component F2 may depend on z but not on x or y, then the work is
= [ "F, dx + [ " F, dy + [ "F.dz. S
W =
If F has only an x component, then Eq. 7-36 reduces to
W =
F(x) dx.
(7-36)
(7-32)
Power The power due to a force is the rate at which that force does work on an object. If the force does work W during a time inter- val At, the average power due to the force over that time interval is
Pavg
W At
Instantaneous power is the instantaneous rate of doing work:
dw P = dt
(7-42)
(7-43)
For a force F at an angle & to the direction of travel of the instan- taneous velocity V, the instantaneous power is
P = Fv cos = F. v.
(7-47,7-48)

    ''',

    '''


Review & Summary
Conservative Forces A force is a conservative force if the net work it does on a particle moving around any closed path, from an initial point and then back to that point, is zero. Equivalently, a force is conservative if the net work it does on a particle moving between two points does not depend on the path taken by the par- ticle. The gravitational force and the spring force are conservative forces; the kinetic frictional force is a nonconservative force.
Potential Energy A potential energy is energy that is associated with the configuration of a system in which a conservative force acts. When the conservative force does work W on a particle within the sys- tem, the change AU in the potential energy of the system is
AU = -W.
(8-1) If the particle moves from point x, to point x,, the change in the potential energy of the system is
AU = − ["F(x) dx.
(8-6)
Gravitational Potential Energy The potential energy asso- ciated with a system consisting of Earth and a nearby particle is gravitational potential energy. If the particle moves from height y; to height y, the change in the gravitational potential energy of the particle-Earth system is
AU= mg(y- y) = mg Ay.
(8-7)
If the reference point of the particle is set as y;= 0 and the cor- responding gravitational potential energy of the system is set as U1 = 0, then the gravitational potential energy U when the parti-
cle is at any height y is
U(y) = mgy.
(8-9)
Elastic Potential Energy Elastic potential energy is the energy associated with the state of compression or extension of an elastic object. For a spring that exerts a spring force F = -kx when its free end has displacement x, the elastic potential energy is
U(x) = kx2.
(8-11)
The reference configuration has the spring at its relaxed length, at which x = 0 and U = 0.
Mechanical Energy The mechanical energy Emec of a system is the sum of its kinetic energy K and potential energy U: Emec = K + U.
(8-12)
An isolated system is one in which no external force causes energy changes. If only conservative forces do work within an isolated sys- tem, then the mechanical energy Emec of the system cannot change. This principle of conservation of mechanical energy is written as (8-17) in which the subscripts refer to different instants during an energy transfer process. This conservation principle can also be written as
K2+ U2 = K1 + U1,
AEmec = AK+ AU = 0.
(8-18)
Potential Energy Curves If we know the potential energy function U(x) for a system in which a one-dimensional force F(x)
200
CHAPTER 8 POTENTIAL ENERGY AND CONSERVATION OF ENERGY
acts on a particle, we can find the force as
F(x)
dU(x) dx
(8-22)
If U(x) is given on a graph, then at any value of x, the force F(x) is the negative of the slope of the curve there and the kinetic energy of the particle is given by
K(x) = Emec - U(x),
(8-24)
where Emec is the mechanical energy of the system. A turning point is a point x at which the particle reverses its motion (there, K = 0). The particle is in equilibrium at points where the slope of the U(x) curve is zero (there, F(x) = 0).
Work Done on a System by an External Force Work W is energy transferred to or from a system by means of an external force acting on the system. When more than one force acts on a system, their net work is the transferred energy. When friction is not involved, the work done on the system and the change AEmec in the mechanical energy of the system are equal:
W = AE mec = AK + AU.
(8-26, 8-25)
When a kinetic frictional force acts within the system, then the ther- mal energy Eh of the system changes. (This energy is associated with the random motion of atoms and molecules in the system.) The work done on the system is then
W=AEmec + AEth
(8-33)
The change AE is related to the magnitude f of the frictional force and the magnitude d of the displacement caused by the external force by (8-31)
AEth=fid.
Conservation of Energy The total energy E of a system (the sum of its mechanical energy and its internal energies, including thermal energy) can change only by amounts of energy that are transferred to or from the system. This experimental fact is known as the law of conservation of energy. If work W is done on the system, then
W = AE = AEmec + AEth + AEint
If the system is isolated (W = 0), this gives
and
AEmec + AEth+AEint = 0 Emec2= Emec,1 AEth - AEint
(8-35)
(8-36) (8-37)
where the subscripts 1 and 2 refer to two different instants. Power The power due to a force is the rate at which that force transfers energy. If an amount of energy AE is transferred by a force in an amount of time At, the average power of the force is ΔΕ Δε
Pavg
The instantaneous power due to a force is
P =
dE dt
(8-40)
(8-41)

    ''',

    '''


Review & Summary
Center of Mass The center of mass of a system of n particles is defined to be the point whose coordinates are given by
or
Χρυσά
M
M
Newton's Second Law for a System of Particles The motion of the center of mass of any system of particles is governed by Newton's second law for a system of particles, which is
=Σ my Zoom-
1
mizi,
M
(9-5)
(9-8)
(9-14) Here is the net force of all the external forces acting on the sys- tem, M is the total mass of the system, and is the acceleration of the system's center of mass.
1
where M is the total mass of the system.
244
CHAPTER 9 CENTER OF MASS AND LINEAR MOMENTUM
Linear Momentum and Newton's Second Law For a sin- gle particle, we define a quantity p called its linear momentum as
(9-22)
must be conserved (it is a constant), which we can write in vector form as (9-50)
and can write Newton's second law in terms of this momentum:
Fret dp
dt
For a system of particles these relations become
(9-23)
P-MV and Fat
dP di
(9-25, 9-27)
Collision and Impulse Applying Newton's second law in momentum form to a particle-like body involved in a collision leads to the impulse-linear momentum theorem:
Pr-Pi-Ap-7,
(9-31,9-32)
where PP-Ap is the change in the body's linear momen- tum, and is the impulse due to the force F(t) exerted on the body by the other body in the collision:
7- Fo) dr.
(9-30)
If Fay is the average magnitude of F(t) during the collision and At is the duration of the collision, then for one-dimensional motion
J-FAL
(9-35)
When a steady stream of bodies, each with mass m and speed v, col- lides with a body whose position is fixed, the average force on the fixed body is
Five-Ap-m Av,
where subscripts i and ƒ refer to values just before and just after the collision, respectively.
If the motion of the bodies is along a single axis, the collision is one-dimensional and we can write Eq. 9-50 in terms of velocity components along that axis:
(9-51)
If the bodies stick together, the collision is a completely inelastic collision and the bodies have the same final velocity V (because they are stuck together).
Motion of the Center of Mass The center of mass of a closed, isolated system of two colliding bodies is not affected by a collision. In particular, the velocity of the center of mass can- not be changed by the collision.
Elastic Collisions in One Dimension
An elastic collision is a special type of collision in which the kinetic energy of a system of colliding bodies is conserved. If the system is closed and isolated, its linear momentum is also conserved. For a one- dimensional collision in which body 2 is a target and body 1 is an incoming projectile, conservation of kinetic energy and linear momentum yield the following expressions for the velocities immediately after the collision:
(9-37)
and
where n/Ar is the rate at which the bodies collide with the fixed body, and Av is the change in velocity of each colliding body. This average force can also be written as
Am Δν, Δε
(9-40)
where Am/Ar is the rate at which mass collides with the fixed body. In Eqs. 9-37 and 9-40, Av-v if the bodies stop upon impact and Av- -2v if they bounce directly backward with no change in their speed.
Conservation of Linear Momentum If a system is isolated so that no net external force acts on it, the linear momentum P of the system remains constant:
P-constant (closed, isolated system).
This can also be written as
PP (closed, isolated system).
(9-42)
(9-43)
where the subscripts refer to the values of P at some initial time and at a later time. Equations 9-42 and 9-43 are equivalent statements of the law of conservation of linear momentum.
Inelastic Collision in One Dimension In an inelastic collision of two bodies, the kinetic energy of the two-body system is not conserved (it is not a constant). If the system is closed and isolated, the total linear momentum of the system
Vu
m1 + m2
2m
Vu
my + m2
(9-67)
(9-68)
Collisions in Two Dimensions If two bodies collide and their motion is not along a single axis (the collision is not head-on), the collision is two-dimensional. If the two-body system is closed and isolated, the law of conservation of momentum applies to the collision and can be written as
P+P-Py+Py
(9-77)
In component form, the law gives two equations that describe the collision (one equation for each of the two dimensions). If the col- lision is also elastic (a special case), the conservation of kinetic en- ergy during the collision gives a third equation:
Ku+K2- K1 + K2-
(9-78)
Variable-Mass Systems In the absence of external forces a rocket accelerates at an instantaneous rate given by
Rved - Ma (first rocket equation).
(9-87)
in which M is the rocket's instantaneous mass (including unexpended fuel), R is the fuel consumption rate, and v is the fuel's exhaust speed relative to the rocket. The term Rv is the thrust of the rocket engine. For a rocket with constant R and V, whose speed changes from v, to vy when its mass changes from M, to My,
M
(second rocket equation).
M
(9-88)

    ''',

    '''


Review & Summary
Angular Position To describe the rotation of a rigid body about a fixed axis, called the rotation axis, we assume a reference line is fixed in the body, perpendicular to that axis and rotating with the body. We measure the angular position of this line relative to a fixed direction. When is measured in radians,
6-
(radian measure),
(10-1) where s is the arc length of a circular path of radius r and angle 6. Radian measure is related to angle measure in revolutions and de- grees by
1 rev - 360° - 2 rad.
(10-2) Angular Displacement A body that rotates about a rotation axis, changing its angular position from 6 to 6, undergoes an angu- lar displacement
40-0-0
(10-4) where A is positive for counterclockwise rotation and negative for
clockwise rotation.
Angular Velocity and Speed If a body rotates through an angular displacement A@ in a time interval Ar, its average angular velocity is
ΔΕ Δε
The (instantaneous) angular velocity of the body is
do dt
(10-5)
(10-6)
Both way and ware vectors, with directions given by the right-hand rule of Fig. 10-6. They are positive for counterclockwise rotation and negative for clockwise rotation. The magnitude of the body's angular velocity is the angular speed.
Angular Acceleration If the angular velocity of a body changes from to an in a time interval A-2-4, the average angular acceleration a... of the body is
4-4
Aa Δε
The (instantaneous) angular acceleration of the body is
Both ag and a are vectors.
dw dt
(10-7)
(10-8)
The Kinematic Equations for Constant Angular Accel- eration Constant angular acceleration (a = constant) is an im- portant special case of rotational motion. The appropriate kine- matic equations, given in Table 10-1, are
(10-12)
(10-13)
a2+2(0-0).
(10-14)
(10-15)
(10-16)
Linear and Angular Variables Related A point in a rigid rotating body, at a perpendicular distance r from the rotation axis,
moves in a circle with radius r. If the body rotates through an angle 6, the point moves along an are with lengths given by sor (radian measure),
where is in radians.
(10-17)
The linear velocity of the point is tangent to the circle; the point's linear speed v is given by
v=aar (radian measure),
(10-18)
where wis the angular speed (in radians per second) of the body. The linear acceleration a of the point has both tangential and radial components. The tangential component is
a, ar (radian measure),
(10-22)
where a is the magnitude of the angular acceleration (in radians per second-squared) of the body. The radial component of a is
a,
(radian measure).
(10-23)
If the point moves in uniform circular motion, the period T of the motion for the point and the body is 2′′ 2π V
T-
(radian measure).
(10-19, 10-20)
Rotational Kinetic Energy and Rotational Inertia The ki- netic energy K of a rigid body rotating about a fixed axis is given by K-a (radian measure), (10-34)
in which / is the rotational inertia of the body, defined as 1- Σ
for a system of discrete particles and defined as
(10-33)
(10-35)
for a body with continuously distributed mass. The r and r, in these expressions represent the perpendicular distance from the axis of rotation to each mass element in the body, and the integration is car- ried out over the entire body so as to include every mass element. The Parallel-Axis Theorem The parallel-axis theorem relates the rotational inertia I of a body about any axis to that of the same body about a parallel axis through the center of mass
I-Icom + Mh2.
(10-36)
Here h is the perpendicular distance between the two axes, and Icom is the rotational inertia of the body about the axis through the com. We can describe h as being the distance the actual rotation axis has been shifted from the rotation axis through the com.
Torque Torque is a turning or twisting action on a body about a ro- tation axis due to a force F. If F is exerted at a point given by the po- sition vector 7 relative to the axis, then the magnitude of the torque is
TrErFrF sin
(10-40, 10-41, 10-39)
where F, is the component of F perpendicular to 7 and is the an- gle between 7 and F. The quantity r, is the perpendicular distance between the rotation axis and an extended line running through the F vector. This line is called the line of action of F, and r, is called the moment arm of F. Similarly, r is the moment arm of F
286
CHAPTER 10 ROTATION
The SI unit of torque is the newton-meter (N·m). A torque is positive if it tends to rotate a body at rest counterclockwise and negative if it tends to rotate the body clockwise.
equations used for translational motion and are
W- 7d0
(10-53)
and
P-
dW dt
(10-55)
(10-45)
When is constant, Eq. 10-53 reduces to
(10-54)
Newton's Second Law in Angular Form The rotational analog of Newton's second law is
T-la,
where he is the net torque acting on a particle or rigid body, I is the ro tational inertia of the particle or body about the rotation axis, and or is the resulting angular acceleration about that axis
Work and Rotational Kinetic Energy The equations used for calculating work and power in rotational motion correspond to
The form of the work-kinetic energy theorem used for rotating bodies is (10-52)
AK-KK-II-W.

    ''',

    '''


Review & Summary
Rolling Bodies For a wheel of radius R rolling smoothly,
VaR,
(11-2) where Vem is the linear speed of the wheel's center of mass and wis the angular speed of the wheel about its center. The wheel may also be viewed as rotating instantaneously about the point P of the "road" that is in contact with the wheel. The angular speed of the wheel about this point is the same as the angular speed of the wheel about its center. The rolling wheel has kinetic energy
K-+M
(11-5) where Icom is the rotational inertia of the wheel about its center of mass and M is the mass of the wheel. If the wheel is being accelerated but is still rolling smoothly, the acceleration of the center of mass com is related to the angular acceleration a about the center with
amaR.
(11-6)
If the wheel rolls smoothly down a ramp of angle 6, its acceleration along an x axis extending up the ramp is
a.com,
g sin @ 1+om/MR
(11-10)
Torque as a Vector In three dimensions, torque 7 is a vector quantity defined relative to a fixed point (usually an origin); it is
(11-14) where F is a force applied to a particle and 7 is a position vector lo- cating the particle relative to the fixed point. The magnitude of Fis - rF sindrF-r_F (11-15, 11-16, 11-17) where ø is the angle between F and 7, F, is the component of F perpendicular to 7, and r, is the moment arm of F. The direction of F is given by the right-hand rule.
QUESTIONS
319
Angular Momentum of a Particle The angular momentum of a particle with linear momentum j, mass m, and linear velocity is a vector quantity defined relative to a fixed point (usually an origin) as
7-7xp-m(7xv).
The magnitude of 7 is given by
e- rmv sin d
- rp1 = rmv
-rip-rmv,
The time rate of change of this angular momentum is equal to the net external torque on the system (the vector sum of the torques due to interactions with particles external to the system):
(11-18)
(system of particles).
dt
(11-29)
(11-19)
(11-20)
(11-21)
Angular Momentum of a Rigid Body For a rigid body rotating about a fixed axis, the component of its angular momentum parallel to the rotation axis is
L-I (rigid body, fixed axis).
(11-31)
where is the angle between 7 and p, p, and v are the compo nents of ō and v perpendicular to 7, and r, is the perpendicular distance between the fixed point and the extension of p. The direc- tion of is given by the right-hand rule for cross products. Newton's Second Law in Angular Form Newton's second law for a particle can be written in angular form as
(11-23)
where is the net torque acting on the particle and is the angu- lar momentum of the particle.
Angular Momentum of a System of Particles The angu- lar momentum Ľ of a system of particles is the vector sum of the angular momenta of the individual particles:
+
Conservation of Angular Momentum The angular mo- mentum Ľ of a system remains constant if the net external torque acting on the system is zero:
or
L-a constant (isolated system) L-L, (isolated system).
This is the law of conservation of angular momentum.
(11-32)
(11-33)
Precession of a Gyroscope A spinning gyroscope can pre- cess about a vertical axis through its support at the rate
Mgr 2 = Iw
(11-46)
(11-26)
where M is the gyroscope's mass, r is the moment arm, I is the rota- tional inertia, and wis the spin rate.
J=1

    ''',

    '''

Review & Summary
Static Equilibrium A rigid body at rest is said to be in static equilibrium. For such a body, the vector sum of the external forces acting on it is zero:
Fet0 (balance of forces).
(12-3)
If all the forces lie in the xy plane, this vector equation is equiva- lent to two component equations:
Feet, and Faty = 0 (balance of forces). Static equilibrium also implies that the vector sum of the external torques acting on the body about any point is zero, or
(12-7, 12-8)
Feet-0 (balance of torques).
(12-5) If the forces lie in the xy plane, all torque vectors are parallel to the z axis, and Eq. 12-5 is equivalent to the single component equation Text: 0 (balance of torques). (12-9)
Center of Gravity The gravitational force acts individually on each element of a body. The net effect of all individual actions may be found by imagining an equivalent total gravitational force F acting at the center of gravity. If the gravitational acceleration g is the same for all the elements of the body, the center of gravity is at the center of mass.
Elastic Moduli Three elastic moduli are used to describe the elastic behavior (deformations) of objects as they respond to forces that act on them. The strain (fractional change in length) is linearly related to the applied stress (force per unit area) by the proper modulus, according to the general relation
stress = modulus X strain.
(12-22)
Tension and Compression When an object is under tension or compression, Eq. 12-22 is written as
AL
(12-23)
where AL/L is the tensile or compressive strain of the object, Fis the magnitude of the applied force F causing the strain, A is the cross-sectional area over which F is applied (perpendicular to A, as in Fig. 12-11a), and E is the Young's modulus for the object. The stress is F/A.
Shearing When an object is under a shearing stress, Eq. 12-22 is
written as
-G
(12-24)
where Ax/L is the shearing strain of the object, Ax is the displacement of one end of the object in the direction of the ap- plied force F (as in Fig. 12-116), and G is the shear modulus of the object. The stress is FIA.
Hydraulic Stress When an object undergoes hydraulic com- pression due to a stress exerted by a surrounding fluid, Eq. 12-22 is written as
(12-25)
where p is the pressure (hydraulic stress) on the object due to the fluid, AVIV (the strain) is the absolute value of the fractional change in the object's volume due to that pressure, and B is the bulk modulus of the object.

    ''',

    '''


Review & Summary
The Law of Gravitation Any particle in the universe attracts any other particle with a gravitational force whose magnitude is F-G- (Newton's law of gravitation),
mm
(13-1)
where my and m2 are the masses of the particles, r is their separation, and G (-6.67 x 10" N-m2/kg) is the gravitational constant Gravitational Behavior of Uniform Spherical Shells The gravitational force between extended bodies is found by adding (integrating) the individual forces on individual particles within the bodies. However, if either of the bodies is a uniform spherical shell or a spherically symmetric solid, the net gravita- tional force it exerts on an external object may be computed as if all the mass of the shell or body were located at its center.
Superposition Gravitational forces obey the principle of su- perposition; that is, if n particles interact, the net force Fat on a particle labeled particle 1 is the sum of the forces on it from all the other particles taken one at a time:
1-2
(13-5)
in which the sum is a vector sum of the forces F1, on particle 1 from particles 2, 3,..., n. The gravitational force F1 on a
particle from an extended body is found by dividing the body into units of differential mass dm, each of which produces a differential force dF on the particle, and then integrating to find the sum of those forces:
F. - Sar
(13-6)
Gravitational Acceleration The gravitational acceleration a, of a particle (of mass m) is due solely to the gravitational force acting on it. When the particle is at distancer from the center of a uniform, spherical body of mass M, the magnitude F of the gravitational force on the particle is given by Eq. 13-1. Thus, by Newton's second law, F-ma
which gives
GM
(13-10)
(13-11)
Free-Fall Acceleration and Weight Because Earth's mass is not distributed uniformly, because the planet is not perfectly spherical, and because it rotates, the actual free-fall acceleration g of a particle near Earth differs slightly from the gravitational accel- eration a, and the particle's weight (equal to mg) differs from the magnitude of the gravitational force on it as calculated by Newton's law of gravitation (Eq. 13-1).
QUESTIONS
377
Gravitation Within a Spherical Shell A uniform shell of matter exerts no net gravitational force on a particle located inside it. This means that if a particle is located inside a uniform solid sphere at distance r from its center, the gravitational force exerted on the particle is due only to the mass that lies inside a sphere of radius r (the inside sphere). The force magnitude is given by
GmM R1
where M is the sphere's mass and R is its radius.
(13-19)
Gravitational Potential Energy The gravitational potential energy U(r) of a system of two particles, with masses M and m and separated by a distance r, is the negative of the work that would be done by the gravitational force of either particle acting on the other if the separation between the particles were changed from infinite (very large) to r. This energy is
GMm
(gravitational potential energy).
(13-21)
Potential Energy of a System If a system contains more than two particles, its total gravitational potential energy U is the sum of the terms representing the potential energies of all the pairs. As an example, for three particles, of masses m1, m2, and m3,
U-
Gmm2 Gm ms 712 713
Gm2my 723
(13-22)
Kepler's Laws The motion of satellites, both natural and artifi- cial, is governed by these laws:
1. The law of orbits. All planets move in elliptical orbits with the Sun at one focus.
2. The law of areas. A line joining any planet to the Sun sweeps out equal areas in equal time intervals. (This statement is equiv alent to conservation of angular momentum.)
3. The law of periods. The square of the period I of any planet is proportional to the cube of the semimajor axis a of its orbit. For circular orbits with radius r,
T-GM
(law of periods),
(13-34)
where M is the mass of the attracting body--the Sun in the case of the solar system. For elliptical planetary orbits, the semi- major axis a is substituted for r.
Energy in Planetary Motion When a planet or satellite with mass m moves in a circular orbit with radius r, its potential energy U and kinetic energy K are given by
The mechanical energy E - K + U is then
E-
GMm 2r
For an elliptical orbit of semimajor axis a,
GMm
U-
and K-
GMm 2r
(13-21, 13-38)
(13-40)
E
GMm 2a
(13-42)
(13-28)
Einstein's View of Gravitation Einstein pointed out that gravi. tation and acceleration are equivalent. This principle of equivalence led him to a theory of gravitation (the general theory of relativity) that explains gravitational effects in terms of a curvature of space.
Escape Speed An object will escape the gravitational pull of an astronomical body of mass M and radius R (that is, it will reach an infinite distance) if the object's speed near the body's surface is at least equal to the escape speed, given by
2GM R

    ''',

    '''


Review & Summary
Density The density p of any material is defined as the material's mass per unit volume:
Am PAV
(14-1)
Usually, where a material sample is much larger than atomic dimensions, we can write Eq. 14-1 as
(14-2)
Fluid Pressure A fluid is a substance that can flow; it conforms to the boundaries of its container because it cannot withstand shear- ing stress. It can, however, exert a force perpendicular to its surface. That force is described in terms of pressure p
AF ΔΑ
(14-3)
in which AF is the force acting on a surface element of area AA. If the force is uniform over a flat area, Eq. 14-3 can be written as
(14-4) a
The force resulting from fluid pressure at a particular point in fluid has the same magnitude in all directions. Gauge pressure is the difference between the actual pressure (or absolute pressure) at a point and the atmospheric pressure.
Pressure Variation with Height and Depth Pressure in a fluid at rest varies with vertical position y. For y measured positive upward, (14-7)
The pressure in a fluid is the same for all points at the same level. If h is the depth of a fluid sample below some reference level at which the pressure is p1, then the pressure in the sample is
P-Po+pgh.
(14-8)
Pascal's Principle A change in the pressure applied to an en- closed fluid is transmitted undiminished to every portion of the fluid and to the walls of the containing vessel.
Archimedes' Principle When a body is fully or partially sub- merged in a fluid, a buoyant force F, from the surrounding fluid acts on the body. The force is directed upward and has a magni- tude given by (14-16)
F-mg.
where m, is the mass of the fluid that has been displaced by the body (that is, the fluid that has been pushed out of the way by the body).
When a body floats in a fluid, the magnitude F, of the (upward) buoyant force on the body is equal to the magnitude F, of the (down- ward) gravitational force on the body. The apparent weight of a body on which a buoyant force acts is related to its actual weight by weight, weight-F
(14-19)
Flow of Ideal Fluids An ideal fluid is incompressible and lacks viscosity, and its flow is steady and irrotational. A streamline is the path followed by an individual fluid particle. A tube of flow is a bundle of streamlines. The flow within any tube of flow obeys the equation of continuity:
Ry- Ava constant,
(14-24)
in which Ry is the volume flow rate, A is the cross-sectional area of the tube of flow at any point, and v is the speed of the fluid at that point. The mass flow rate R., is
RpRy-pAv- a constant.
(14-25)
Bernoulli's Equation Applying the principle of conservation of mechanical energy to the flow of an ideal fluid leads to Bernoulli's equation along any tube of flow:
p+pv2+pgy a constant.
(14-29)

    ''',

    '''


Review & Summary
Frequency The frequency fof periodic, or oscillatory, motion is the number of oscillations per second. In the SI system, it is mea- sured in hertz:
(15-1)
1 hertz = 1 Hz= 1 oscillation per second = 1 s1. Period The period T is the time required for one complete oscil- lation, or cycle. It is related to the frequency by
1
T
(15-2)
Simple Harmonic Motion In simple harmonic motion (SHM), the displacement x(t) of a particle from its equilibrium position is described by the equation
x = xm cos(wt + )
(displacement),
(15-3)
in which x, is the amplitude of the displacement, wt + is the phase of the motion, and is the phase constant. The angular fre- quency w is related to the period and frequency of the motion by
2πf (angular frequency).
2π (15-5) T Differentiating Eq. 15-3 leads to equations for the particle's SHM velocity and acceleration as functions of time:
and
v=wx sin(wt + ) (velocity)
a = w2xm cos(wt+) (acceleration).
(15-6)
(15-7)
In Eq. 15-6, the positive quantity aut, is the velocity amplitude V of the motion. In Eq. 15-7, the positive quantity axis the acceler- ation amplitude am of the motion.
The Linear Oscillator A particle with mass m that moves un- der the influence of a Hooke's law restoring force given by F = -kx exhibits simple harmonic motion with
and
k
@=
(angular frequency)
m
T = 2π
m k
(period).
(15-12)
(15-13)
Such a system is called a linear simple harmonic oscillator. Energy A particle in simple harmonic motion has, at any time, kinetic energy K = m2 and potential energy U = kx2. If no fric- tion is present, the mechanical energy E = K+ U remains con- stant even though K and U change.
Pendulums Examples of devices that undergo simple harmonic motion are the torsion pendulum of Fig. 15-9, the simple pendulum of Fig. 15-11, and the physical pendulum of Fig. 15-12. Their periods of oscillation for small oscillations are, respectively, T = 2π VIIK (torsion pendulum).
T = 2π VL/g
(simple pendulum),
T=2π VI/mgh (physical pendulum).
(15-23)
(15-28)
(15-29)
Simple Harmonic Motion and Uniform Circular Motion Simple harmonic motion is the projection of uniform circular motion onto the diameter of the circle in which the circular motion occurs. Figure 15-15 shows that all parameters of circular motion (position, velocity, and acceleration) project to the corresponding values for simple harmonic motion.
Damped Harmonic Motion The mechanical energy E in a real oscillating system decreases during the oscillations because external forces, such as a drag force, inhibit the oscillations and transfer me- chanical energy to thermal energy. The real oscillator and its motion are then said to be damped. If the damping force is given by F1 = -by, where v is the velocity of the oscillator and b is a damping con- stant, then the displacement of the oscillator is given by
x(t) = xm e-b2m cos(w't + ),
(15-42)
where, the angular frequency of the damped oscillator, is given by
k
b2
m
4m2
(15-43)
If the damping constant is small (b < √km), then w≈ w, where w is the angular frequency of the undamped oscillator. For small b, the mechanical energy E of the oscillator is given by
E(t)=kx2me
-bt/m
(15-44) Forced Oscillations and Resonance If an external driving force with angular frequency, acts on an oscillating sys- tem with natural angular frequency w, the system oscillates with angular frequency . The velocity amplitude v of the system is greatest when
wd = w,
(15-46)
a condition called resonance. The amplitude x of the system is (approximately) greatest under the same condition.

    ''',

    '''


Review & Summary
Transverse and Longitudinal Waves Mechanical waves can exist only in material media and are governed by Newton's laws. Transverse mechanical waves, like those on a stretched string, are waves in which the particles of the medium oscillate perpendi- cular to the wave's direction of travel. Waves in which the particles of the medium oscillate parallel to the wave's direction of travel are longitudinal waves.
Sinusoidal Waves A sinusoidal wave moving in the positive direction of an x axis has the mathematical form
y(x, t) = ym sin(kx – wt),
(16-2) where y, is the amplitude of the wave, k is the angular wave number, w is the angular frequency, and kx - wt is the phase. The wavelength A is related to k by
k
2π λ
The period T and frequency ƒ of the wave are related to w by
ω
2π
1 Τ
Finally, the wave speed v is related to these other parameters by
=
k
λ T
(16-5)
(16-9)
(16-13)
Equation of a Traveling Wave Any function of the form
y(x, t) = h(kx = wt)
(16-17) can represent a traveling wave with a wave speed given by Eq. 16-13 and a wave shape given by the mathematical form of h. The plus sign denotes a wave traveling in the negative direction of the x axis, and the minus sign a wave traveling in the positive direction.
Wave Speed on Stretched String The speed of a wave on a stretched string is set by properties of the string. The speed on a string with tension and linear density μ is
v =
(16-26)
Power The average power of, or average rate at which energy is transmitted by, a sinusoidal wave on a stretched string is given by Pavguvay (16-33)
Superposition of Waves When two or more waves traverse the same medium, the displacement of any particle of the medium is the sum of the displacements that the individual waves would give it. Interference of Waves Two sinusoidal waves on the same string exhibit interference, adding or canceling according to the prin- ciple of superposition. If the two are traveling in the same direction and have the same amplitude ym and frequency (hence the same wavelength) but differ in phase by a phase constant 6, the result is a single wave with this same frequency:
-
y'(x,t) = [2y, cosø] sin(kx − at +48).
(16-51)
If = 0, the waves are exactly in phase and their interference is fully constructive; if = #rad, they are exactly out of phase and their interference is fully destructive.
Phasors A wave y(x, t) can be represented with a phasor. This is a vector that has a magnitude equal to the amplitude ym of the wave and that rotates about an origin with an angular speed equal to the angular frequency @ of the wave. The projection of the rotat- ing phasor on a vertical axis gives the displacement y of a point along the wave's travel.
Standing Waves The interference of two identical sinusoidal waves moving in opposite directions produces standing waves. For a string with fixed ends, the standing wave is given by y'(x, t) = [2y, sin kx] cos wt.
(16-60) Standing waves are characterized by fixed locations of zero dis- placement called nodes and fixed locations of maximum displace- ment called antinodes.
Resonance Standing waves on a string can be set up by reflection of traveling waves from the ends of the string. If an end is fixed, it must be the position of a node. This limits the frequen- cies at which standing waves will occur on a given string. Each pos- sible frequency is a resonant frequency, and the corresponding standing wave pattern is an oscillation mode. For a stretched string of length L with fixed ends, the resonant frequencies are for n = 1, 2, 3,....
ν
ν
λ
-= n 2L'
(16-66)
The oscillation mode corresponding to n = 1 is called the funda- mental mode or the first harmonic; the mode corresponding to n = 2 is the second harmonic; and so on.

    ''',

    '''

    Review & Summary
Sound Waves Sound waves are longitudinal mechanical waves that can travel through solids, liquids, or gases. The speed v of a sound wave in a medium having bulk modulus B and density pis
B
(speed of sound).
In air at 20°C, the speed of sound is 343 m/s.
(17-3)
A sound wave causes a longitudinal displacements of a mass element in a medium as given by
-
S=5, cos(kx-t),
(17-12)
where s,, is the displacement amplitude (maximum displacement) from equilibrium, k-2/A, and w-2πf, A and ƒ being the wave- length and frequency of the sound wave. The wave also causes a pressure change Ap from the equilibrium pressure:
Ap Ap, sin(kx-out),
where the pressure amplitude is
Apm - (vpw)
(17-13)
(17-14)
Interference The interference of two sound waves with identi- cal wavelengths passing through a common point depends on their phase difference & there. If the sound waves were emitted in phase and are traveling in approximately the same direction, is given by AL λ
(17-21)
where AL is their path length difference (the difference in the distances traveled by the waves to reach the common point). Fully constructive interference occurs when is an integer multiple of 2,
-m(2), for m -0,1,2,...,
and, equivalently, when AL is related to wavelength A by AL
0,1,2,...
A
(17-22)
(17-23)
Fully destructive interference occurs when is an odd multiple of #, (17-24)
=(2m+1), for m0,1,2,...,
and, equivalently, when AL is related to A by
AL
-0.5,1.5,2.5,....
(17-25) Sound Intensity The intensity I of a sound wave at a surface is the average rate per unit area at which energy is transferred by the wave through or onto the surface:
(17-26)
where P is the time rate of energy transfer (power) of the sound wave
and A is the area of the surface intercepting the sound. The intensity I
is related to the displacement amplitudes,, of the sound wave by
I-pva's
(17-27) The intensity at a distancer from a point source that emits sound waves of power P, is
1-
(17-28)
Sound Level in Decibels The sound level ẞ in decibels (dB) is defined as
6- (10 dB) log
(17-29)
where 1, (-10-12 W/m2) is a reference intensity level to which all intensities are compared. For every factor-of-10 increase in inten- sity, 10 dB is added to the sound level.
Standing Wave Patterns in Pipes Standing sound wave patterns can be set up in pipes. A pipe open at both ends will resonate at frequencies
nv 2L
n-1,2,3,...,
(17-39)
where v is the speed of sound in the air in the pipe. For a pipe closed at one end and open at the other, the resonant fre- quencies are
ην 4L
n-1,3,5,....
(17-41)
Beats Beats arise when two waves having slightly different fre- quencies, f, and f2, are detected together. The beat frequency is
(17-46)
The Doppler Effect The Doppler effect is a change in the observed frequency of a wave when the source or the detec tor moves relative to the transmitting medium (such as air). For sound the observed frequency f'" is given in terms of the source frequency/by
V vs
(general Doppler effect),
(17-47)
where vo is the speed of the detector relative to the medium, vg is that of the source, and v is the speed of sound in the medium. The signs are chosen such that f' tends to be greater for motion toward and less for motion away.
Shock Wave If the speed of a source relative to the medium exceeds the speed of sound in the medium, the Doppler equation no longer applies. In such a case, shock waves result. The half-angle 6 of the Mach cone is given by
sin -
Vs
(Mach cone angle).
(17-57)

    ''',

    '''

    Review & Summary
Temperature; Thermometers Temperature is an SI base quantity related to our sense of hot and cold. It is measured with a thermometer, which contains a working substance with a measur able property, such as length or pressure, that changes in a regular way as the substance becomes hotter or colder.
Zeroth Law of Thermodynamics When a thermometer and some other object are placed in contact with each other, they even- tually reach thermal equilibrium. The reading of the thermometer is then taken to be the temperature of the other object. The process provides consistent and useful temperature measurements because of the zeroth law of thermodynamics: If bodies A and B are each in thermal equilibrium with a third body C (the thermometer), then A and B are in thermal equilibrium with each other.
The Kelvin Temperature Scale In the SI system, tempera- ture is measured on the Kelvin scale, which is based on the triple point of water (273.16 K). Other temperatures are then defined by
use of a constant-volume gas thermometer, in which a sample of gas is maintained at constant volume so its pressure is proportional to its temperature. We define the temperature T as measured with a gas thermometer to be
T-(273.16 K) (lim
Ps
(18-6)
Here T is in kelvins, and p, and p are the pressures of the gas at 273.16 K and the measured temperature, respectively.
Celsius and Fahrenheit Scales The Celsius temperature scale is defined by
Tc-T-273.15°,
with T'in kelvins. The Fahrenheit temperature scale is defined by T-TC+32°.
(18-7)
(18-8)
REVIEW & SUMMARY
539
Thermal Expansion All objects change size with changes in tem- perature. For a temperature change AT, a change AL in any linear dimension Lis given by
AL - La AT,
(18-9)
in which a is the coefficient of linear expansion. The change AV in the volume V of a solid or liquid is
AV - VBAT.
The integration is necessary because the pressure p may vary dur- ing the volume change.
First Law of Thermodynamics The principle of conser vation of energy for a thermodynamic process is expressed in the first law of thermodynamics, which may assume either of the forms
(18-10)
or
Here ẞ - 3a is the material's coefficient of volume expansion.
Heat Heat Q is energy that is transferred between a system and its environment because of a temperature difference between them. It can be measured in joules (J), calories (cal), kilocalories (Cal or kcal), or British thermal units (Btu), with
1 cal - 3.968 x 10 Btu - 4.1868 J.
(18-12)
Heat Capacity and Specific Heat If heat Q is absorbed by an object, the object's temperature change T/T, is related to Q by
Q-C(T-T).
(18-13)
in which C is the heat capacity of the object. If the object has mass m, then
Q-cm(T-T),
(18-14)
where c is the specific heat of the material making up the object. The molar specific heat of a material is the heat capacity per mole, which means per 6.02 x 1023 elementary units of the material.
Heat of Transformation Matter can exist in three common states: solid, liquid, and vapor. Heat absorbed by a material may change the material's physical state-for example, from solid to liq- uid or from liquid to gas. The amount of energy required per unit mass to change the state (but not the temperature) of a particular material is its heat of transformation L. Thus,
Q-Lm.
(18-16)
The heat of vaporization L, is the amount of energy per unit mass that must be added to vaporize a liquid or that must be removed to condense a gas. The heat of fusion L is the amount of energy per unit mass that must be added to melt a solid or that must be re- moved to freeze a liquid.
Work Associated with Volume Change A gas may exchange energy with its surroundings through work. The amount of work W done by a gas as it expands or contracts from an initial volume V, to a final volume V, is given by
W- dW- pdV.
(18-25)
AE-EE-Q-W dEdQ-dw
(first law)
(18-26)
(first law).
(18-27)
E represents the internal energy of the material, which depends only on the material's state (temperature, pressure, and volume). Q represents the energy exchanged as heat between the system and its surroundings; Q is positive if the system absorbs heat and negative if the system loses heat. W is the work done by the sys- tem; W is positive if the system expands against an external force from the surroundings and negative if the system contracts be- cause of an external force. Q and W are path dependent; AE is path independent.
Applications of the First Law The first law of thermody- namics finds application in several special cases:
adiabatic processes: Q-0, AE-W constant-volume processes: W-0, AE-Q
cyclical processes: AE-0, 0-w free expansions: Q-W-AE-0
Conduction, Convection, and Radiation The rate Podat which energy is conducted through a slab for which one face is maintained at the higher temperature Ty, and the other face is maintained at the lower temperature Teis
Pond -- KA TH-Ic
L
(18-32)
Here each face of the slab has area A, the length of the slab (the distance between the faces) is L, and k is the thermal conductivity of the material.
Convection occurs when temperature differences cause an en- ergy transfer by motion within a fluid.
Radiation is an energy transfer via the emission of electromag- netic energy. The rate P at which an object emits energy via ther- mal radiation is
Pro-EAT,
(18-38)
where (-5.6704 × 10 W/m2K) is the Stefan-Boltzmann constant, is the emissivity of the object's surface, A is its surface area, and T is its surface temperature (in kelvins). The rate Pabu at which an object absorbs energy via thermal radiation from its envi- ronment, which is at the uniform temperature T... (in kelvins), is (18-39)
Pats-σEAT

    ''',

    '''

    Review & Summary
Kinetic Theory of Gases The kinetic theory of gases relates the macroscopic properties of gases (for example, pressure and temperature) to the microscopic properties of gas molecules (for example, speed and kinetic energy).
Avogadro's Number One mole of a substance contains Na (Avogadro's number) elementary units (usually atoms or mole- cules), where N, is found experimentally to be
N-6.02 x 10 mol-1
(Avogadro's number). (19-1)
One molar mass M of any substance is the mass of one mole of the substance. It is related to the mass m of the individual molecules of the substance by (19-4)
M-mNa
The number of moles n contained in a sample of mass Mum consisting of N molecules, is given by
N Mn Mu
(19-2, 19-3)
NA
M
mNA
576
CHAPTER 19 THE KINETIC THEORY OF GASES
Ideal Gas An ideal gas is one for which the pressure p, volume V, and temperature T'are related by
pV = nRT (ideal gas law).
a gas are
Vang-
8RT V M
(average speed),
(19-31)
(19-5)
2RT
Vp
M
(most probable speed).
(19-35)
Here n is the number of moles of the gas present and R is a constant (8.31 J/mol·K) called the gas constant. The ideal gas law can also be
written as
pV - NkT,
where the Boltzmann constant kis
138 x 10-J/K.
NA
(19-9)
(19-7)
and the rms speed defined above in Eq. 19-22.
Molar Specific Heats The molar specific heat Cy of a gas at constant volume is defined as
ΔΕ
η ΔΤ
nAT
(19-39, 19-41)
Work in an Isothermal Volume Change The work done by an ideal gas during an isothermal (constant-temperature) change from volume V, to volume V, is
W-ART In (ideal gas, isothermal process). (19-14)
Pressure, Temperature, and Molecular Speed The pres- sure exerted by n moles of an ideal gas, in terms of the speed of its molecules, is
3V
(19-21) where V-V(v) is the root-mean-square speed of the mole- cules of the gas. With Eq. 19-5 this gives
in which is the energy transferred as heat to or from a sample of n moles of the gas, AT is the resulting temperature change of the gas, and AE is the resulting change in the internal energy of the gas. For an ideal monatomic gas,
CVR 12.5 J/mol K.
"AT'
(19-43)
The molar specific heat C, of a gas at constant pressure is defined to be (19-46) in which Q, n, and AT are defined as above. C, is also given by C-Cy+R.
For n moles of an ideal gas, EnCyT
(ideal gas).
(19-22)
(19-49)
(19-44)
3RT M
Temperature and Kinetic Energy The average transla- tional kinetic energy Kay per molecule of an ideal gas is
Kay-KT.
(19-24)
Mean Free Path The mean free path A of a gas molecule is its average path length between collisions and is given by
(19-25)
1 √2m2 N/V where N/V is the number of molecules per unit volume and d is the molecular diameter.
Maxwell Speed Distribution The Maxwell speed distri- bution P(v) is a function such that P(v) dv gives the fraction of molecules with speeds in the interval dv at speed v:
P(v)-4-
M 2RT
(19-27)
Three measures of the distribution of speeds among the molecules of
If a moles of a confined ideal gas undergo a temperature change AT due to any process, the change in the internal energy of the gas is (19-45)
AEst-nCAT (ideal gas, any process).
Degrees of Freedom and Cy The equipartition of energy theorem states that every degree of freedom of a molecule has an energy kT per molecule (-RT per mole). If f is the number of degrees of freedom, then E-(f/2)nRT and
C-(4)R
R 4.16f J/mol K.
(19-51)
For monatomic gases f-3 (three translational degrees); for di- atomic gases f = 5 (three translational and two rotational degrees). Adiabatic Process When an ideal gas undergoes an adiabatic volume change (a change for which Q = 0),
pV-a constant (adiabatic process),
(19-53)
in which y(-C/C) is the ratio of molar specific heats for the gas. For a free expansion, however, pV a constant.

    ''',

    '''

    Review & Summary
One-Way Processes An irreversible process is one that can- not be reversed by means of small changes in the environment. The direction in which an irreversible process proceeds is set by the change in entropy AS of the system undergoing the process. Entropy S is a state property (or state function) of the system; that is, it depends only on the state of the system and not on the way in which the system reached that state. The entropy postulate states (in part): If an irreversible process occurs in a closed system, the entropy of the system always increases
Calculating Entropy Change The entropy change AS for an irreversible process that takes a system from an initial state i to a final state fis exactly equal to the entropy change AS for any re- versible process that takes the system between those same two states. We can compute the latter (but not the former) with
(20-1)
Here is the energy transferred as heat to or from the system dur- ing the process, and T is the temperature of the system in kelvins during the process.
For a reversible isothermal process, Eq. 20-1 reduces to
(20-2)
When the temperature change AT of a system is small relative to the temperature (in kelvins) before and after the process, the en- tropy change can be approximated as
AS-S-S
TINE
(20-3)
where T., is the system's average temperature during the process. When an ideal gas changes reversibly from an initial state with temperature T, and volume V, to a final state with temperature T and volume V,, the change AS in the entropy of the gas is
V1
AS-S, - S1 = nR In+nC, In-
T T
(20-4)
The Second Law of Thermodynamics This law, which is an extension of the entropy postulate, states: If a process occurs in a closed system, the entropy of the system increases for irreversible processes and remains constant for reversible processes. It never de- creases. In equation form,
AS ≥ 0.
(20-5)
Engines An engine is a device that, operating in a cycle, extracts energy as heat IQH from a high-temperature reservoir and does a cer- tain amount of work W. The efficiency of any engine is defined as W energy we get (20-11) energy we pay for
In an ideal engine, all processes are reversible and no wasteful energy transfers occur due to, say, friction and turbulence. A Carnot engine is an ideal engine that follows the cycle of Fig. 20-9. Its efficiency is
1
TH
(20-12, 20-13)
in which T and T are the temperatures of the high- and low- temperature reservoirs, respectively. Real engines always have an efficiency lower than that given by Eq. 20-13. Ideal engines that are not Carnot engines also have lower efficiencies.
A perfect engine is an imaginary engine in which energy ex- tracted as heat from the high-temperature reservoir is converted com- pletely to work. Such an engine would violate the second law of ther- modynamics, which can be restated as follows: No series of processes is possible whose sole result is the absorption of energy as heat from a thermal reservoir and the complete conversion of this energy to work. Refrigerators A refrigerator is a device that, operating in a cy- cle, has work W done on it as it extracts energy IQ as heat from a low-temperature reservoir. The coefficient of performance K of a refrigerator is defined as
what we want
what we pay for
W
(20-14)
A Carnot refrigerator is a Carnot engine operating in reverse.
QUESTIONS
603
For a Carnot refrigerator, Eq. 20-14 becomes
Ke
ел
T TH-T
(20-15, 20-16)
A perfect refrigerator is an imaginary refrigerator in which energy extracted as heat from the low-temperature reservoir is con- verted completely to heat discharged to the high-temperature reser- voir, without any need for work. Such a refrigerator would violate the second law of thermodynamics, which can be restated as follows: No series of processes is possible whose sole result is the transfer of energy as heat from a reservoir at a given temperature to a reservoir at a higher temperature.
Entropy from a Statistical View The entropy of a system can be defined in terms of the possible distributions of its molecules. For identical molecules, each possible distribution of molecules is called a microstate of the system. All equivalent microstates are grouped into
a configuration of the system. The number of microstates in a config- uration is the multiplicity W of the configuration.
For a system of N molecules that may be distributed between the two halves of a box, the multiplicity is given by
N!
W-
(20-20)
in which n, is the number of molecules in one half of the box and n2 is the number in the other half. A basic assumption of statistical mechanics is that all the microstates are equally probable. Thus, con- figurations with a large multiplicity occur most often.
The multiplicity W of a configuration of a system and the en- tropy S of the system in that configuration are related by Boltzmann's entropy equation:
S-k In W,
where k = 1.38 x 10-2 J/K is the Boltzmann constant.
(20-21)

    ''',

    '''

    Review & Summary
Electric Charge The strength of a particle's electrical interaction with objects around it depends on its electric charge (usually repre- sented as q), which can be either positive or negative. Particles with the same sign of charge repel each other, and particles with opposite signs of charge attract each other. An object with equal amounts of the two kinds of charge is electrically neutral, whereas one with an imbalance is electrically charged and has an excess charge.
Conductors are materials in which a significant number of electrons are free to move. The charged particles in nonconductors (insulators) are not free to move.
Electric current i is the rate dq/dt at which charge passes a point: (electric current).
dg i- dt
(21-3)
Coulomb's Law Coulomb's law describes the electrostatic force (or electric force) between two charged particles. If the parti- cles have charges q, and 92, are separated by distance r, and are at rest (or moving only slowly) relative to each other, then the magni- tude of the force acting on each due to the other is given by
19:
4 TE
(Coulomb's law),
(21-4)
where - 8.85 x 10-12 C/N m2 is the permittivity constant. The ratio 1/4, is often replaced with the electrostatic constant (or Coulomb constant) k=8.99 x 10°N m2/C2.
The electrostatic force vector acting on a charged particle due to a second charged particle is either directly toward the second particle (opposite signs of charge) or directly away from it (same sign of charge). As with other types of forces, if multiple electrostatic forces act on a particle, the net force is the vector sum (not scalar sum) of the individual forces.
The two shell theories for electrostatics are
Shell theorem 1: A charged particle outside a shell with charge uniformly distributed on its surface is attracted or repelled as if the shell's charge were concentrated as a particle at its center. Shell theorem 2: A charged particle inside a shell with charge uniformly distributed on its surface has no net force acting on it due to the shell.
Charge on a conducting spherical shell spreads uniformly over the (external) surface.
The Elementary Charge Electric charge is quantized (re- stricted to certain values). The charge of a particle can be written as ne, where n is a positive or negative integer and e is the elemen- tary charge, which is the magnitude of the charge of the electron and proton (-1.602 × 10-19 C).
Conservation of Charge The net electric charge of any iso- lated system is always conserved.

    ''',

    '''

    Review & Summary
Electric Field To explain the electrostatic force between two charges, we assume that each charge sets up an electric field in the space around it. The force acting on each charge is then due to the electric field set up at its location by the other charge.
Definition of Electric Field The electric field E at any point is defined in terms of the electrostatic force ♬ that would be ex- erted on a positive test charge qoplaced there:
(22-1)
Electric Field Lines Electric field lines provide a means for visu- alizing the direction and magnitude of electric fields. The electric field vector at any point is tangent to a field line through that point. The density of field lines in any region is proportional to the magnitude of the electric field in that region. Field lines originate on positive charges and terminate on negative charges.
Field Due to a Point Charge The magnitude of the electric field E set up by a point charge q at a distance / from the charge is
1
E-
4m r2
(22-3)
The direction of E is away from the point charge if the charge is positive and toward it if the charge is negative.
Field Due to an Electric Dipole An electric dipole consists of two particles with charges of equal magnitude q but opposite sign, separated by a small distance d. Their electric dipole moment p has magnitude qd and points from the negative charge to the positive charge. The magnitude of the electric field set up by the dipole at a distant point on the dipole axis (which runs through both charges) is
E-
2m 21
(22-9)
where z is the distance between the point and the center of the dipole.
Field Due to a Continuous Charge Distribution The electric field due to a continuous charge distribution is found by treating charge elements as point charges and then summing, via integration, the electric field vectors produced by all the charge el- ements to find the net vector.
QUESTIONS
651
Field Due to a Charged Disk The electric field magnitude at a point on the central axis through a uniformly charged disk is given by
2
(22-26)
where z is the distance along the axis from the center of the disk, R is the radius of the disk, and is the surface charge density.
Force on a Point Charge in an Electric Field When a point charge q is placed in an external electric field E, the electro- static force F that acts on the point charge is
Force F has the same direction as E if q is positive and the opposite direction if q is negative.
Dipole in an Electric Field When an electric dipole of dipole moment ♬ is placed in an electric field E, the field exerts a torque 7 on the dipole:
(22-34)
The dipole has a potential energy U associated with its orientation in the field:
U--p.Ē.
(22-28)
(22-38) This potential energy is defined to be zero when is perpendicular to E; it is least (UPE) when p is aligned with E and greatest (U-PE) when is directed opposite E.

    ''',

    '''

    Review & Summary
Gauss' Law Gauss' law and Coulomb's law are different ways of describing the relation between charge and electric field in static situations. Gauss' law is
-
(Gauss' law),
(23-6)
in which gene is the net charge inside an imaginary closed surface (a Gaussian surface) and is the net flux of the electric field through the surface:
0-9 E-dA
(electric flux through a Gaussian surface).
(23-4)
with uniform linear charge density A is perpendicular to the line of charge and has magnitude
E
(line of charge).
2 mar
(23-12)
where r is the perpendicular distance from the line of charge to the point.
4. The electric field due to an infinite nonconducting sheet with
uniform surface charge density or is perpendicular to the plane of the sheet and has magnitude
σ
Coulomb's law can be derived from Gauss' law.
Applications of Gauss' Law Using Gauss' law and, in some cases, symmetry arguments, we can derive several important results in electrostatic situations. Among these are:
1. An excess charge on an isolated conductor is located entirely on the outer surface of the conductor.
2. The external electric field near the surface of a charged conductor is perpendicular to the surface and has a magnitude that depends on the surface charge density o
E- (conducting surface).
Within the conductor, E = 0.
(23-11)
3. The electric field at any point due to an infinite line of charge
E-
(sheet of charge).
200
(23-13)
5. The electric field outside a spherical shell of charge with radius R and total charge q is directed radially and has magnitude
4m
(spherical shell, for r = R).
(23-15)
Here r is the distance from the center of the shell to the point at which E is measured. (The charge behaves, for external points, as if it were all located at the center of the sphere.) The field inside a uniform spherical shell of charge is exactly zero:
E-0 (spherical shell, for r < R).
(23-16)
6. The electric field inside a uniform sphere of charge is directed radially and has magnitude
E-
4 WER
(23-20)

    ''',

    '''

    Review & Summary
Electric Potential The electric potential V at a point P in the electric field of a charged object is
-W
40
(24-2)
where W. is the work that would be done by the electric force on a positive test charge were it brought from an infinite distance to P, and U is the potential energy that would then be stored in the test charge-object system.
Electric Potential Energy If a particle with charge q is placed at a point where the electric potential of a charged object is V, the electric potential energy U of the particle-object system is
U-qV.
(24-3)
If the particle moves through a potential difference AV, the change in the electric potential energy is
AU-qAV = q(V-Vi
(24-4)
Mechanical Energy If a particle moves through a change AV in electric potential without an applied force acting on it, applying the conservation of mechanical energy gives the change in kinetic energy as (24-9)
AK- -qAV.
If, instead, an applied force acts on the particle, doing work Wapp the change in kinetic energy is
AK--qAV + Wapp
(24-11)
In the special case when AK-0, the work of an applied force
708
CHAPTER 24 ELECTRIC POTENTIAL
involves only the motion of the particle through a potential difference:
Wapp-qAV (for K-K).
(24-12)
Equipotential Surfaces The points on an equipotential sur- face all have the same electric potential. The work done on a test charge in moving it from one such surface to another is independent of the locations of the initial and final points on these surfaces and of the path that joins the points. The electric field E is always directed perpendicularly to corresponding equipotential surfaces.
Finding V from E The electric potential difference between two points / and fis
ds,
(24-18)
where the integral is taken over any path connecting the points. If the integration is difficult along any particular path, we can choose a differ- ent path along which the integration might be easier. If we choose V,- 0, we have, for the potential at a particular point,
v-- fx. dr.
(24-19)
In the special case of a uniform field of magnitude E, the po tential change between two adjacent (parallel) equipotential lines separated by distance Ax is
AV--EAX.
(24-21)
Potential Due to a Charged Particle The electric potential due to a single charged particle at a distance r from that particle is (24-26)
14 4T
where V has the same sign as q. The potential due to a collection of charged particles is
v-v-
41
(24-27)
Potential Due to an Electric Dipole At a distance r from an electric dipole with dipole moment magnitude pqd, the elec- tric potential of the dipole is
1
p cos @
V-
(24-30)
4 TE
شو
for r >> d; the angle is defined in Fig. 24-13. Potential Due to a Continuous Charge Distribution For a continuous distribution of charge, Eq. 24-27 becomes
(24-32)
in which the integral is taken over the entire distribution. Calculating E from V The component of E in any direction is the negative of the rate at which the potential changes with dis- tance in that direction:
av
E
as
The x, y, and z components of E may be found from
(24-40)
av
E,
av ду
av
E-
(24-41)
az
E, When E is uniform, Eq. 24-40 reduces to
E-
AV As
(24-42)
where s is perpendicular to the equipotential surfaces. Electric Potential Energy of a System of Charged Particles The electric potential energy of a system of charged particles is equal to the work needed to assemble the system with the particles initially at rest and infinitely distant from each other. For two particles at separation r
U-W- 1992
4 TE
(24-46)
Potential of a Charged Conductor An excess charge placed on a conductor will, in the equilibrium state, be located entirely on the outer surface of the conductor. The charge will distribute itself so that the following occur: (1) The entire conductor, including interior points, is at a uniform potential. (2) At every internal point, the elec tric field due to the charge cancels the external electric field that oth- erwise would have been there. (3) The net electric field at every point on the surface is perpendicular to the surface.

    ''',

    '''

    Review & Summary
Capacitor; Capacitance A capacitor consists of two isolated conductors (the plates) with charges +q and -q. Its capacitance C is defined from
q-CV,
where V is the potential difference between the plates.
(25-1)
Determining Capacitance We generally determine the capacitance of a particular capacitor configuration by (1) assuming a charge q to have been placed on the plates, (2) finding the electric field E due to this charge, (3) evaluating the potential difference V, and (4) calculating C from Eq. 25-1. Some specific results are the following: A parallel-plate capacitor with flat parallel plates of area A and spacing d has capacitance
C-
EA d
(25-9)
A cylindrical capacitor (two long coaxial cylinders) of length Land radii a and b has capacitance
C-2
L In(b/a)
(25-14)
A spherical capacitor with concentric spherical plates of radii a and b has capacitance
C-4
ab b-a
An isolated sphere of radius R has capacitance
C-4 R.
(25-17)
(25-18)
Capacitors in Parallel and in Series The equivalent capacitances C. of combinations of individual capacitors con- nected in parallel and in series can be found from
Ca
Equivalent capacitances can be used to calculate the capacitances of more complicated series-parallel combinations.
Potential Energy and Energy Density The electric poten- tial energy U of a charged capacitor,
2C
(25-21, 25-22)
is equal to the work required to charge the capacitor. This energy can be associated with the capacitor's electric field E. By extension we can associate stored energy with any electric field. In vacuum, the energy density, or potential energy per unit volume, within an electric field of magnitude E is given by
(25-25)
Capacitance with a Dielectric If the space between the plates of a capacitor is completely filled with a dielectric material, the capacitance C is increased by a factor x, called the dielectric constant, which is characteristic of the material. In a region that is completely filled by a dielectric, all electrostatic equations con- taining must be modified by replacing with K-
The effects of adding a dielectric can be understood physically in terms of the action of an electric field on the permanent or induced electric dipoles in the dielectric slab. The result is the for- mation of induced charges on the surfaces of the dielectric, which results in a weakening of the field within the dielectric for a given amount of free charge on the plates.
Gauss' Law with a Dielectric When a dielectric is present, Gauss' law may be generalized to
-C (n capacitors in parallel)
(25-19)
1-1
q.
(25-36)
and
Сод
ΣΕ
(n capacitors in series).
(25-20)
Here q is the free charge; any induced surface charge is accounted for by including the dielectric constant inside the integral.

    '''
]

chem_text = [

    '''

    Fundamental Laws of Chemistry
Conservation of Mass – In any chemical reaction, the total mass of reactants equals the total mass of products. Matter is neither created nor destroyed.
Law of Definite Proportions – A given chemical compound always contains its component elements in fixed, definite ratios by mass, regardless of sample size or source.
Law of Multiple Proportions – When two elements form multiple compounds, the mass of one element that combines with a fixed mass of the other follows simple whole-number ratios.
Dalton’s Atomic Theory
Atomic Composition – All elements consist of indivisible, fundamental particles called atoms.
Elemental Identity – Atoms of the same element are identical in mass and properties, while atoms of different elements have distinct characteristics.
Compound Formation – Chemical compounds result from the combination of atoms in fixed, whole-number ratios.
Chemical Reactions – Atoms are neither created nor destroyed in chemical reactions; they rearrange to form new substances, maintaining mass conservation.
Early Atomic Models and Experiments
Thomson’s Plum Pudding Model – Proposed that atoms consist of negatively charged electrons embedded within a diffuse, positively charged sphere.
Millikan’s Oil Drop Experiment – Determined the charge of a single electron by measuring the behavior of tiny oil droplets in an electric field.
Rutherford’s Gold Foil Experiment – Demonstrated that atoms have a dense, positively charged nucleus, disproving the plum pudding model by showing that most of an atom’s volume is empty space.
Nuclear Model of the Atom – Proposed by Rutherford, describing the atom as a small, central nucleus surrounded by electrons moving in empty space.
Atomic Structure
Nucleus – A compact, dense region at the center of the atom containing:
Protons – Positively charged particles, each with a relative mass of 1 atomic mass unit (amu).
Neutrons – Electrically neutral particles with nearly the same mass as protons.
Electrons – Negatively charged particles residing in the space around the nucleus, with a mass approximately 1/1840 that of a proton.
Isotopes – Variants of an element with the same number of protons but different numbers of neutrons, leading to different mass numbers.
Chemical Bonding and Molecular Structure
Covalent Bonds – Formed when atoms share electrons to create molecules.
Molecular Representation:
Chemical Formula – Denotes the number and type of atoms in a molecule.
Structural Formula – Shows the specific arrangement of atoms.
Ball-and-Stick Model – Illustrates spatial relationships between atoms.
Space-Filling Model – Represents the actual relative sizes of atoms in a molecule.
Formation of Ions and Ionic Bonding
Cation Formation – An atom loses one or more electrons, acquiring a positive charge.
Anion Formation – An atom gains one or more electrons, acquiring a negative charge.
Ionic Bonds – Strong electrostatic forces between oppositely charged cations and anions, forming ionic compounds.
The Periodic Table and Element Classification
Elements are arranged by increasing atomic number, grouping those with similar properties into columns (groups).
Metals – Form cations, generally conductive, malleable, and ductile.
Nonmetals – Form anions, often brittle solids or gases, poor conductors.
Naming Chemical Compounds
Binary Compounds – Composed of two elements:
Type I – Metal with a fixed oxidation state (e.g., NaCl, MgO).
Type II – Metal with variable oxidation states, indicated by Roman numerals (e.g., FeCl₂ = Iron(II) chloride).
Type III – Two nonmetals, named using Greek prefixes (e.g., CO₂ = Carbon dioxide).
Polyatomic Ions – Charged species consisting of multiple atoms bonded together, forming ionic compounds (e.g., NH₄⁺, SO₄²⁻).

''',

'''

Stoichiometry: Quantitative Relationships in Chemical Reactions
Definition – Stoichiometry examines the numerical relationships between reactants and products in chemical reactions, determining the amounts of substances consumed or produced.
Counting Atoms by Mass – Since individual atoms are too small to count directly, their quantity is inferred by measuring mass.
Mass-Number Relationship – To convert between mass and the number of atoms, the average atomic mass (weighted based on isotopic abundance) is essential.
The Mole: The Fundamental Counting Unit in Chemistry
Definition – A mole represents 6.022 × 10²³ (Avogadro’s number) of any specified particles (atoms, molecules, ions, or formula units).
Carbon-12 Standard – One mole is defined as the number of carbon atoms in exactly 12 g of pure carbon-12 (
12
12
 C).
Mass-Mole Relationship – The molar mass of an element, measured in grams per mole (g/mol), is numerically equivalent to its atomic mass in atomic mass units (amu).
Molar Mass: Mass of One Mole of a Substance
Definition – The mass of 1 mole of a substance (element or compound) in grams.
Calculation for Compounds – Determined by summing the atomic masses of constituent atoms based on their chemical formula.
Percent Composition: Elemental Distribution in a Compound
Definition – The mass percent of each element in a given compound.
Formula:
Mass percent
=
(
Mass of element in 1 mole of substance
Mass of 1 mole of substance
)
×
100
%
Mass percent=( 
Mass of 1 mole of substance
Mass of element in 1 mole of substance
​	
 )×100%
Empirical and Molecular Formulas
Empirical Formula: Simplest Atomic Ratio

Definition – Represents the simplest whole-number ratio of different types of atoms in a compound.
Derivation – Can be determined using the percent composition of the compound.
Molecular Formula: Actual Molecular Composition

For Molecular Substances – Specifies the actual number of atoms in a single molecule. It is always a whole-number multiple of the empirical formula.
For Ionic Substances – The molecular formula is identical to the empirical formula, as ionic compounds do not form discrete molecules.
Chemical Reactions: Transformation of Substances
Definition – A process where reactants are converted into products through the breaking and formation of chemical bonds.
Law of Conservation of Mass – Atoms cannot be created or destroyed in a reaction; all atoms in the reactants must also appear in the products.
Chemical Equations: Representation of Reactions
Definition – A symbolic representation of a chemical reaction.
Structure:
Reactants are listed on the left side.
Products are listed on the right side.
The arrow (→) signifies the direction of the reaction.
Balanced Chemical Equation – Ensures the law of conservation of mass by maintaining equal numbers of each atom on both sides.
Stoichiometric Calculations: Determining Reactant and Product Quantities
Balanced Equations as Conversion Factors – The coefficients in a balanced chemical equation provide the mole ratio between reactants and products.
Limiting Reactant Concept:
The limiting reactant is the first reactant to be fully consumed, restricting the maximum amount of product formed.
The excess reactant remains after the reaction is complete.
Yield: Efficiency of a Chemical Reaction
Theoretical Yield – The maximum amount of product that could be produced based on complete reaction of the limiting reactant.
Actual Yield – The measured amount of product obtained from the reaction, which is always lower than the theoretical yield due to inefficiencies.
Percent Yield Formula:
Percent yield
=
(
Actual yield
Theoretical yield
)
×
100
%
Percent yield=( 
Theoretical yield
Actual yield
​	
 )×100%

''',

'''

Hydrocarbons: Structure, Classification, and Reactivity
Hydrocarbons are organic compounds composed primarily of carbon and hydrogen atoms. They can exist as linear chains, branched structures, or cyclic (ring-shaped) molecules. These compounds serve as the foundation of organic chemistry and can be classified based on the type of bonds between carbon atoms.

Alkanes: Saturated Hydrocarbons

Definition – Alkanes are hydrocarbons that contain only carbon-carbon single bonds (C–C).
General Formula – Given by CₙH₂ₙ₊₂, where n represents the number of carbon atoms.
Saturation – Called saturated hydrocarbons because each carbon atom forms four single bonds, ensuring the maximum possible number of hydrogen atoms.
Hybridization – Carbon atoms in alkanes exhibit sp³ hybridization, forming tetrahedral molecular geometries.
Isomerism – Alkanes can form structural isomers, where the same molecular formula corresponds to different branching arrangements.
Reactivity:
Combustion Reaction – Alkanes react with oxygen (O₂) to form carbon dioxide (CO₂) and water (H₂O), releasing energy.
Substitution Reactions – Alkanes can undergo halogenation, where a hydrogen atom is replaced by a halogen (e.g., chlorine or bromine).
Alkenes: Unsaturated Hydrocarbons with Double Bonds

Definition – Alkenes contain at least one carbon-carbon double bond (C=C).
Simplest Example – Ethene (C₂H₄, also called ethylene), where carbon atoms are sp² hybridized and arranged in a trigonal planar geometry.
Isomerism – The double bond prevents free rotation, leading to the formation of cis-trans (geometric) isomers based on the arrangement of substituents around the double bond.
Reactivity –
Addition Reactions – Alkenes readily react with substances such as hydrogen (H₂), halogens (Br₂, Cl₂), and hydrogen halides (HCl, HBr) by breaking the double bond and forming new single bonds.
Alkynes: Unsaturated Hydrocarbons with Triple Bonds

Definition – Alkynes contain at least one carbon-carbon triple bond (C≡C).
Simplest Example – Ethyne (C₂H₂, also called acetylene), where carbon atoms exhibit sp hybridization, forming a linear geometry.
Reactivity – Like alkenes, alkynes undergo addition reactions, breaking the triple bond to form more saturated products.
Aromatic Hydrocarbons: Resonance-Stabilized Rings

Definition – These hydrocarbons contain ring structures with delocalized π electrons, following Hückel’s Rule (4n+2 π electrons).
Reactivity – Unlike alkenes and alkynes, they undergo substitution reactions (e.g., electrophilic aromatic substitution) rather than addition, preserving the aromatic ring stability.
Hydrocarbon Derivatives: Functional Groups and Reactivity
Hydrocarbon derivatives are organic compounds that contain additional functional groups, modifying their chemical properties.

Common Functional Groups

Alcohols – Contain the –OH (hydroxyl) group, making them polar and capable of hydrogen bonding.
Aldehydes – Characterized by the carbonyl group (C=O) at the end of a carbon chain.
Carboxylic Acids – Contain both carbonyl (C=O) and hydroxyl (–OH) groups, contributing to acidity.
Polymers: Macromolecules from Repeating Units
Polymers are large molecules formed by linking small repeating units (monomers).

Types of Polymerization

Addition Polymerization – Monomers with double bonds undergo a chain reaction mechanism, leading to polymer growth (e.g., polyethylene, polypropylene).
Condensation Polymerization – Monomers link together while eliminating a small molecule (e.g., water), forming polymers like proteins and polyesters.
Proteins: Biological Polymers and Structural Organization
Proteins are essential natural polymers with molar masses ranging from 600 to over 1,000,000 g/mol.

''',

'''

Electrolytes
Strong Electrolyte:
Completely dissociates in solution to produce separate ions (e.g., NaCl → Na⁺ + Cl⁻).
Conducts electricity very efficiently due to the high concentration of ions.
Common examples include soluble salts (like NaCl), strong acids (like HCl), and strong bases (like NaOH).
Weak Electrolyte:
Only a small fraction of dissolved molecules dissociate into ions (e.g., CH₃COOH ↔ CH₃COO⁻ + H⁺).
Conducts electricity poorly, as there are fewer ions present in solution.
Common examples include weak acids (like acetic acid) and weak bases (like ammonia).
Nonelectrolyte:
Dissolved substances that do not produce ions in solution (e.g., sugar, ethanol).
Does not conduct electricity as there are no free ions present.
Acids and Bases
Arrhenius Model:
Acid: A substance that, when dissolved in water, produces hydrogen ions (H⁺).
Base: A substance that, when dissolved in water, produces hydroxide ions (OH⁻).
Brønsted–Lowry Model:
Acid: A proton donor, which can transfer a hydrogen ion to another substance.
Base: A proton acceptor, which can accept a hydrogen ion from another substance.
Strong Acid:
Completely dissociates in solution to yield H⁺ ions and anions (e.g., HCl → H⁺ + Cl⁻).
High conductivity due to a large number of ions.
Weak Acid:
Only partially dissociates in solution, resulting in an equilibrium between undissociated acid and ions (e.g., CH₃COOH ⇌ CH₃COO⁻ + H⁺).
Molarity
Definition: Molarity (M) is a way to express the concentration of a solution.
Formula: Molarity (M) = moles of solute / volume of solution (L).
Standard Solution:
A solution whose concentration is precisely known, often used as a reference in titrations and calculations.
Dilution
Process: Involves adding solvent to a solution to decrease its concentration.
Moles of Solute:
The number of moles of solute remains constant before and after dilution:
Dilution Equation: M₁V₁ = M₂V₂, where M is molarity and V is volume.
Types of Equations that Describe Solution Reactions
Formula Equation:
Represents all reactants and products in their complete formulas, showing the overall reaction without indicating ionic dissociation.
Complete Ionic Equation:
Breaks down strong electrolytes into their constituent ions, showing all ions present in the reaction.
Net Ionic Equation:
Displays only the ions and compounds that undergo a change during the reaction, excluding spectator ions that do not participate.
Solubility Rules
General Observations:
Based on experimental data to predict whether a compound will dissolve in water.
Help in anticipating the formation of precipitates in reactions.
Important Types of Solution Reactions
Acid–Base Reactions:
Characterized by the transfer of H⁺ ions between reactants, often resulting in the formation of water and a salt.
Precipitation Reactions:
Involve the formation of an insoluble solid (precipitate) from the reaction of two soluble reactants.
Oxidation–Reduction Reactions:
Involve the transfer of electrons between substances, resulting in changes to their oxidation states.
Titrations
Definition: A laboratory technique used to determine the concentration of a solution by reacting it with a standard solution of known concentration (the titrant).
Stoichiometric (Equivalence) Point:
The point in the titration at which the amount of titrant added is exactly enough to react with the substance being analyzed.
Endpoint:
The stage in a titration where a visible change occurs, often indicated by a color change due to a chemical indicator.
Oxidation–Reduction Reactions
Oxidation States:
Assigned according to a set of rules to track electron movement during reactions.
Oxidation:
The process where an atom or ion loses electrons, resulting in an increase in oxidation state.
Reduction:
The process where an atom or ion gains electrons, resulting in a decrease in oxidation state.
Oxidizing Agent:
The species that gains electrons in a redox reaction and is thereby reduced.
Reducing Agent:
The species that loses electrons in a redox reaction and is thereby oxidized.
Balancing Equations:
Equations for oxidation-reduction reactions can be balanced using the oxidation states method to ensure mass and charge conservation.

''',

'''

State of a Gas
The state of a gas can be fully described by the following parameters:
Pressure (P): The force exerted by gas particles colliding with the walls of their container per unit area.
Volume (V): The space occupied by the gas.
Temperature (T): A measure of the average kinetic energy of gas particles, expressed in Kelvin (K).
Amount of Gas (n): The quantity of gas present, measured in moles.
Pressure
Common Units of Pressure:
SI Unit: Pascal (Pa)
Other Units:
1 torr = 1 mm Hg
1 atm = 760 torr
1 atm = 101,325 Pa
Gas Laws
Gas laws describe the relationships between pressure, volume, temperature, and amount of gas based on empirical observations.
Boyle’s Law:
Describes the inverse relationship between pressure and volume at constant temperature.
Equation: 
P
V
=
k
PV=k (where 
k
k is a constant).
Charles’s Law:
Describes the direct relationship between volume and temperature at constant pressure.
Equation: 
V
=
b
T
V=bT (where 
b
b is a constant).
Avogadro’s Law:
States that the volume of a gas is directly proportional to the number of moles of gas at constant temperature and pressure.
Equation: 
V
=
a
n
V=an (where 
a
a is a constant).
Ideal Gas Law:
Combines the previous laws into one equation that relates pressure, volume, temperature, and the number of moles of gas.
Equation: 
P
V
=
n
R
T
PV=nRT (where 
R
R is the ideal gas constant).
Partial Pressure:
In a mixture of gases, the partial pressure of component 
n
n is the pressure that gas would exert if it occupied the entire volume alone.
Equation: 
P
total
=
P
1
+
P
2
+
P
3
+
…
P 
total
​	
 =P 
1
​	
 +P 
2
​	
 +P 
3
​	
 +…, where 
P
n
P 
n
​	
  represents the partial pressure of each gas.
Assumptions of Ideal Gases
The ideal gas model makes several key assumptions:
The volume of gas particles is negligible (considered zero).
There are no intermolecular forces or interactions between gas particles.
Gas particles are in constant, random motion and collide elastically with the walls of the container, producing pressure.
The average kinetic energy of gas particles is directly proportional to the absolute temperature of the gas in Kelvin.
Gas Properties
Velocity Distribution:
The particles in a gas sample have a range of velocities, which can be described by the root mean square (rms) velocity.
Root Mean Square (rms) Velocity:
Represents the square root of the average of the squares of the particle velocities.
Equation: 
u
rms
=
3
R
T
M
u 
rms
​	
 = 
M
3RT
​	
 
​	
 , where 
R
R is the ideal gas constant, 
T
T is the temperature in Kelvin, and 
M
M is the molar mass of the gas.
Diffusion:
The process in which gas particles intermingle due to random motion, leading to the gradual mixing of different gases.
Effusion:
The process in which gas particles escape through a small hole into an empty chamber, dependent on the speed of the particles.
Real Gas Behavior
Deviation from Ideal Behavior:
Real gases deviate from ideal behavior at high pressures and low temperatures due to increased particle interactions and volume effects.
Modifications to Ideal Gas Equation:
To accurately describe real gas behavior, modifications must be made to the ideal gas equation to account for:
Intermolecular forces between gas particles.
The actual volume occupied by gas particles.
Van der Waals Equation:
Van der Waals developed an equation that adjusts the ideal gas law to account for these factors:
(
P
+
a
n
2
V
2
)
(
V
−
n
b
)
=
n
R
T
(P+a 
V 
2
 
n 
2
 
​	
 )(V−nb)=nRT
Here, 
a
a accounts for attractive forces between particles, and 
b
b accounts for the volume occupied by the gas particles themselves.

''',

'''

Electromagnetic Radiation
Definition: Electromagnetic radiation is energy that travels through space as waves. It is characterized by three key properties:
Wavelength (λ): The distance between successive peaks of the wave, usually measured in meters (m).
Frequency (ν): The number of wave cycles that pass a point in one second, measured in hertz (Hz).
Speed (c): The speed of light in a vacuum, approximately 
c
=
2.9979
×
10
8
 
m/s
c=2.9979×10 
8
 m/s.
Relationship: The wavelength and frequency are inversely related by the equation:
c
=
λ
ν
c=λν
Photons: Electromagnetic radiation can also be viewed as a stream of particles known as photons. Each photon carries a quantized amount of energy, given by the equation:
E
=
h
ν
E=hν
where 
h
h is Planck's constant (
h
=
6.626
×
10
−
34
 
J s
h=6.626×10 
−34
 J s).
Photoelectric Effect
Definition: The photoelectric effect is the phenomenon where electrons are emitted from a metal surface when it is illuminated by light of sufficient frequency.
Observations:
The kinetic energy of the emitted electrons is dependent on the frequency of the incident light, not its intensity.
This effect demonstrated that light has particle-like properties, leading to the concept that electromagnetic radiation can be considered as a stream of photons.
Hydrogen Spectrum
Emission Spectrum: The emission spectrum of hydrogen consists of distinct lines corresponding to specific wavelengths of light emitted when electrons transition between energy levels.
Significance: The presence of discrete wavelengths indicates that hydrogen has quantized energy levels, where electrons can occupy specific states without intermediate values.
Bohr Model of the Hydrogen Atom
Development: Using data from the hydrogen spectrum and assuming that angular momentum is quantized, Niels Bohr developed a model of the hydrogen atom where:
Electrons travel in fixed circular orbits around the nucleus.
The energy of each orbit is quantized, with electrons emitting or absorbing energy in discrete amounts when transitioning between orbits.
Limitations: Although revolutionary at the time, the Bohr model was ultimately found to be incorrect and insufficient for explaining more complex atoms.
Wave (Quantum) Mechanical Model
Electron Behavior: In this model, electrons are treated as standing waves rather than particles, leading to a more comprehensive understanding of their behavior in atoms.
Wave Function: The square of the wave function (
Ψ
Ψ) describes the probability distribution of an electron's position, providing a statistical interpretation of electron locations rather than definitive paths.
Heisenberg Uncertainty Principle: This principle states that it is impossible to simultaneously know both the exact position and momentum of a particle, which reinforces the probabilistic nature of the quantum mechanical model.
Orbitals: Probability maps derived from the wave function define the shapes and orientations of orbitals, characterized by the quantum numbers:
n (principal quantum number): Indicates the energy level and size of the orbital.
l (azimuthal quantum number): Indicates the shape of the orbital.
mₗ (magnetic quantum number): Indicates the orientation of the orbital in space.
Electron Spin
Spin Quantum Number (
m
s
m 
s
​	
 ): Describes the intrinsic angular momentum of an electron, with possible values of 
+
1
2
+ 
2
1
​	
  or 
−
1
2
− 
2
1
​	
 .
Pauli Exclusion Principle: States that no two electrons in an atom can have the same set of quantum numbers (
n
,
l
,
m
l
,
m
s
n,l,m 
l
​	
 ,m 
s
​	
 ), meaning that only two electrons with opposite spins can occupy the same orbital.
Periodic Table
Aufbau Principle: The order in which orbitals are filled with electrons follows the Aufbau principle, which explains the structure of the periodic table based on the arrangement of electrons in orbitals.
Valence Electrons: Atoms in the same group of the periodic table have the same valence electron configuration, which contributes to their similar chemical properties.
Trends in Properties: Trends such as ionization energy and atomic radius can be explained through concepts of:
Nuclear Attraction: The attractive force between protons in the nucleus and electrons.
Electron Repulsions: The repulsive forces between electrons in the same atom.
Shielding: The effect of inner-shell electrons reducing the effective nuclear charge felt by outer-shell electrons.
Penetration: The ability of an electron in a given orbital to get close to the nucleus, influencing its energy and stability.

''',

'''

Chemical Bonds
Definition: Chemical bonds are the forces that hold groups of atoms together in a compound. They occur when a group of atoms can lower its total energy by aggregating.
Types of Chemical Bonds:
Ionic Bonds: Formed when electrons are transferred from one atom to another, resulting in the formation of charged ions (cations and anions).
Covalent Bonds: Formed by the equal sharing of electrons between two nonmetal atoms.
Polar Covalent Bonds: Occur when electrons are shared unequally between two atoms, leading to a partial positive charge on one atom and a partial negative charge on the other.
Percent Ionic Character: The degree of ionic character in a bond 
X-O-Y
X-O-Y can be measured using the following formula:
Percent Ionic Character
=
(
Measured Dipole Moment of 
X
−
Y
Calculated Dipole Moment for 
X
1
Y
2
)
×
100
%
Percent Ionic Character=( 
Calculated Dipole Moment for X 
1
 Y 
2
 
Measured Dipole Moment of X−Y
​	
 )×100%
Electronegativity: A measure of the relative ability of an atom to attract shared electrons in a chemical bond. The difference in electronegativity between two bonded atoms determines the polarity of the bond:
A larger difference indicates a more polar bond, while a smaller difference suggests a nonpolar bond.
Dipole Moment: The spatial arrangement of polar bonds in a molecule determines whether the molecule has an overall dipole moment, affecting its physical and chemical properties.
Ionic Bonding
Ionic Compounds: Formed from the electrostatic attraction between cations and anions.
Ionic Size:
Anion: An ion formed by the gain of electrons; it is larger than its parent atom due to increased electron-electron repulsion.
Cation: An ion formed by the loss of electrons; it is smaller than its parent atom due to decreased electron-electron repulsion and increased nuclear charge effect.
Lattice Energy: The energy change that occurs when ions are packed together to form an ionic solid. It is a measure of the stability of the ionic compound, with higher lattice energies indicating stronger ionic bonds.
Bond Energy
Definition: The amount of energy required to break a covalent bond between two atoms in a molecule.
Trends:
Bond energy increases with the number of shared electron pairs (e.g., triple bonds have higher bond energy than double bonds, which in turn are stronger than single bonds).
Application: Bond energy can be used to estimate the enthalpy change (ΔH) for a chemical reaction by summing the bond energies of the bonds broken and formed during the reaction.
Lewis Structures
Purpose: Lewis structures visually represent how the valence electron pairs are arranged among atoms in a molecule or polyatomic ion.
Key Concepts:
Stable molecules generally have filled valence orbitals.
Duet Rule: For hydrogen, stability is achieved with two electrons (a filled 1s orbital).
Octet Rule: For second-row elements, stability is typically achieved with eight electrons in the valence shell.
Atoms of elements in the third row and beyond can exceed the octet rule by accommodating more than eight electrons due to available d orbitals.
Resonance: Some molecules can be represented by multiple equivalent Lewis structures, indicating delocalized electrons.
Formal Charge: When multiple nonequivalent Lewis structures can be drawn, formal charge calculations help identify the most stable structure(s) by minimizing formal charges across atoms.
VSEPR Model (Valence Shell Electron Pair Repulsion)
Principle: The VSEPR model is based on the idea that electron pairs (bonding and lone pairs) will arrange themselves around a central atom to minimize electron-electron repulsions, resulting in specific molecular geometries.
Application: The VSEPR model can be used to predict the geometric structure of most molecules, including:
Linear (180°)
Trigonal planar (120°)
Tetrahedral (109.5°)
Trigonal bipyramidal (90° and 120°)
Octahedral (90°)

''',

'''

Two Widely Used Bonding Models
Localized Electron Model
Molecular Orbital Model
Localized Electron Model
Concept: The localized electron model visualizes a molecule as a collection of atoms that share electron pairs between their atomic orbitals. This model emphasizes the role of hybridization in determining molecular structure.
Hybrid Orbitals: To explain the geometry of molecules, hybrid orbitals—combinations of the native atomic orbitals—are often employed. The required hybrid orbitals depend on the number of electron pairs surrounding the central atom:
Six Electron Pairs (Octahedral Arrangement): Require d²sp³ hybrid orbitals.
Five Electron Pairs (Trigonal Bipyramidal Arrangement): Require dsp³ hybrid orbitals.
Four Electron Pairs (Tetrahedral Arrangement): Require sp³ hybrid orbitals.
Three Electron Pairs (Trigonal Planar Arrangement): Require sp² hybrid orbitals.
Two Electron Pairs (Linear Arrangement): Require sp hybrid orbitals.
Types of Bonds:
Sigma (σ) Bonds: Formed when electrons are shared in an area centered along the line connecting the two atoms. This bond type allows for free rotation about the bond axis.
Pi (π) Bonds: Formed when a shared electron pair occupies regions above and below the line connecting the two atoms. These bonds do not allow for free rotation due to their orientation.
Molecular Orbital Model
Concept: The molecular orbital model treats a molecule as a new entity made up of positively charged nuclei and electrons. Instead of focusing solely on localized electron pairs, this model considers electrons to be distributed in molecular orbitals (MOs) that are formed from the atomic orbitals of the constituent atoms.
Key Features:
Delocalization: Electrons in the molecular orbital model are depicted as being delocalized across the entire molecule, which provides a more accurate representation of bonding in polyatomic molecules.
Predictive Power: This model effectively predicts relative bond strength, magnetism, and bond polarity.
Disadvantages: The primary drawback of the molecular orbital model is that it can be challenging to apply qualitatively to polyatomic molecules due to its complexity.
Classification of Molecular Orbitals
Molecular orbitals can be classified based on two main criteria: energy and shape.

Energy:
Bonding Molecular Orbitals (MOs): These MOs are lower in energy than the atomic orbitals from which they are formed. Electrons in bonding MOs are lower in energy within the molecule than in the separated atoms, favoring molecule formation.
Antibonding Molecular Orbitals: These MOs are higher in energy than the atomic orbitals from which they are formed. Electrons in antibonding MOs are higher in energy in the molecule than in the separated atoms, which does not favor molecule formation.
Shape (Symmetry):
Sigma (σ) MOs: These orbitals have their electron probability concentrated along a line passing through the nuclei of the atoms.
Pi (π) MOs: These orbitals have their electron probability distributed above and below the line connecting the nuclei, indicating the presence of a nodal plane.
Bond Order and Resonance
Bond Order: An index of bond strength calculated using the formula:
Bond Order
=
Number of Bonding Electrons
−
Number of Antibonding Electrons
2
Bond Order= 
2
Number of Bonding Electrons−Number of Antibonding Electrons
​	
 
A higher bond order indicates a stronger bond between atoms.
Combining Models: For molecules requiring resonance in the localized electron model, a more accurate description can be achieved by integrating both the localized electron and molecular orbital models:
σ Bonds: Considered localized.
π Bonds: Treated as delocalized.

''',

'''

Condensed States of Matter: Liquids and Solids
General Properties: Liquids and solids are held together by intermolecular forces among their constituent molecules, atoms, or ions. These forces dictate various physical properties, such as surface tension, capillary action, and viscosity in liquids.
Intermolecular Forces
Dipole-Dipole Forces:
Definition: Attractions that occur between molecules with permanent dipole moments.
Hydrogen Bonding: A particularly strong type of dipole-dipole interaction that occurs in molecules where hydrogen is bonded to highly electronegative elements such as nitrogen, oxygen, or fluorine. Hydrogen bonds contribute to unusually high boiling points in substances like water.
London Dispersion Forces:
Definition: Weak attractions that arise from instantaneous dipoles that occur in atoms or nonpolar molecules due to temporary fluctuations in electron distribution. These forces increase with the size of the molecule.
Crystalline Solids
Structure: Crystalline solids are characterized by a regular arrangement of their components, often depicted as a lattice. The smallest repeating unit of the lattice is known as the unit cell.
Classification by Component Types:
Atomic Solids: Composed of individual atoms.
Ionic Solids: Comprised of ions held together by ionic bonds.
Molecular Solids: Formed from molecules held together by intermolecular forces.
Analysis: The arrangement of components in crystalline solids can be determined using X-ray analysis.
Metals
Structure: Metallic solids are modeled by assuming atoms are uniform spheres arranged in a closely packed structure.
Packing Types:
Hexagonal Closest Packing
Cubic Closest Packing
Metallic Bonding Models:
Electron Sea Model: Valence electrons are delocalized and move freely among the metal cations, contributing to conductivity and malleability.
Band Model: Electrons occupy molecular orbitals, forming bands.
Conduction Bands: Closely spaced molecular orbitals with available electron states that facilitate electrical conductivity.
Alloys: Mixtures of metals that exhibit metallic properties.
Types:
Substitutional Alloys: Atoms of one metal are replaced by atoms of another metal of similar size.
Interstitial Alloys: Smaller atoms occupy the spaces between larger metal atoms.
Network Solids
Description: Network solids are characterized by extensive networks of atoms that are covalently bonded together.
Examples:
Diamond: A form of carbon where each atom is tetrahedrally bonded to four other carbon atoms, resulting in a very hard structure.
Graphite: Composed of layers of carbon atoms arranged in a planar hexagonal structure, allowing for slip between layers.
Silicates: Network solids containing silicon-oxygen (Si-O) bridges that form the basis of many rocks, clays, and ceramics.
Semiconductors
Doping Process: Very pure silicon is doped with other elements to modify its electrical properties.
n-type Semiconductors: Created by doping silicon with atoms that have five valence electrons, resulting in excess electrons.
p-type Semiconductors: Created by doping silicon with atoms that have three valence electrons, resulting in "holes" that can carry a positive charge.
Application: Modern electronics rely on devices that utilize p-n junctions formed by combining n-type and p-type materials.
Molecular Solids
Definition: Composed of discrete molecules held together by relatively weak intermolecular forces, resulting in lower boiling and melting points compared to other solid types.
Ionic Solids
Characteristics: Composed of ions held together by strong ionic bonds, resulting in high melting and boiling points. The arrangement typically involves the closest packing of larger ions, with smaller ions occupying tetrahedral or octahedral holes.
Phase Changes
Vaporization: The process of transitioning from liquid to gas (vapor).
Condensation: The reverse process of vaporization, where gas transitions back to liquid.
Equilibrium Vapor Pressure: The pressure exerted by a vapor in equilibrium with its liquid or solid phase in a closed system when the rate of evaporation equals the rate of condensation.
Properties of Liquids: Liquids with high intermolecular forces exhibit relatively low vapor pressures.
Normal Boiling Point: The temperature at which the vapor pressure of a liquid equals one atmosphere.
Normal Melting Point: The temperature at which a solid and its liquid phase have the same vapor pressure at one atmosphere of external pressure.
Phase Diagrams
Function: Illustrate the state of a substance (solid, liquid, gas) at various temperatures and pressures in a closed system.
Key Points:
Triple Point: The unique temperature and pressure at which all three phases coexist in equilibrium.
Critical Point: Defined by critical temperature and pressure, beyond which a gas cannot be liquefied regardless of the pressure applied.
Critical Temperature: The highest temperature at which a substance can exist as a liquid.

''',

'''

Solution Composition
Molarity (M):
Defined as the number of moles of solute per liter of solution.
Formula: 
M
=
moles of solute
liters of solution
M= 
liters of solution
moles of solute
​	
 
Mass Percent:
The ratio of the mass of the solute to the mass of the solution, expressed as a percentage.
Formula: 
Mass percent
=
(
mass of solute
mass of solution
)
×
100
%
Mass percent=( 
mass of solution
mass of solute
​	
 )×100%
Mole Fraction (x):
The ratio of the number of moles of a given component to the total number of moles of all components in the solution.
Formula: 
x
=
moles of component
total moles of all components
x= 
total moles of all components
moles of component
​	
 
Molality (m):
Defined as the number of moles of solute per kilogram of solvent.
Formula: 
m
=
moles of solute
mass of solvent (kg)
m= 
mass of solvent (kg)
moles of solute
​	
 
Normality (N):
The number of equivalents of solute per liter of solution.
Useful in acid-base reactions and redox reactions.
Enthalpy of Solution (
Δ
H
s
o
l
n
ΔH 
soln
​	
 )
Definition: The enthalpy change that occurs when a solution is formed from its components.
Components:
The energy required to overcome solute-solute interactions.
The energy required to create space (or "holes") in the solvent.
The energy associated with the interactions between solute and solvent.
Factors Affecting Solubility
Polarity of Solute and Solvent:
General Rule: “Like dissolves like,” meaning polar solutes dissolve well in polar solvents, while nonpolar solutes dissolve in nonpolar solvents.
Pressure:
Increasing pressure enhances the solubility of gases in a solvent.
Henry’s Law: 
C
=
k
P
C=kP
Where 
C
C is the concentration of the gas, 
k
k is Henry’s law constant, and 
P
P is the partial pressure of the gas.
Temperature Effects:
Increased temperature generally decreases the solubility of gases in water.
Most solids are more soluble at higher temperatures, although there are important exceptions (e.g., certain salts).
Vapor Pressure of Solutions
A solution containing a nonvolatile solute will have a lower vapor pressure compared to that of the pure solvent.
Raoult’s Law:
Defines an ideal solution:
P
s
o
l
n
=
x
⋅
P
p
u
r
e
P 
soln
​	
 =x⋅P 
pure
​	
 
Where 
P
s
o
l
n
P 
soln
​	
  is the vapor pressure of the solution, 
x
x is the mole fraction of the solvent, and 
P
p
u
r
e
P 
pure
​	
  is the vapor pressure of the pure solvent.
Solutions where solute-solvent attractions differ significantly from solute-solute and solvent-solvent attractions will violate Raoult’s law.
Colligative Properties
Definition: Properties that depend on the number of solute particles in a solution rather than their identity.
Key Properties:
Boiling-Point Elevation:
Δ
T
b
=
K
b
⋅
m
s
o
l
u
t
e
ΔT 
b
​	
 =K 
b
​	
 ⋅m 
solute
​	
 
Where 
K
b
K 
b
​	
  is the boiling point elevation constant and 
m
s
o
l
u
t
e
m 
solute
​	
  is the molality of the solute.
Freezing-Point Lowering:
Δ
T
f
=
K
f
⋅
m
s
o
l
u
t
e
ΔT 
f
​	
 =K 
f
​	
 ⋅m 
solute
​	
 
Where 
K
f
K 
f
​	
  is the freezing point depression constant.
Osmotic Pressure:
P
=
M
R
T
P=MRT
Where 
P
P is the osmotic pressure, 
M
M is the molarity, 
R
R is the ideal gas constant, and 
T
T is the temperature in Kelvin.
Osmosis: Occurs when a solution and pure solvent are separated by a semipermeable membrane that allows solvent molecules to pass but not solute particles.
Reverse Osmosis: Happens when pressure applied to the solution exceeds its osmotic pressure, causing solvent to flow from the solution to the pure solvent side.
Van’t Hoff Factor (i):
Represents the number of ions produced by each formula unit of solute when it dissolves.
Colligative properties are affected proportionally to the number of ions produced.
Colloids
Definition: A colloid is a suspension of tiny particles dispersed throughout a continuous medium (liquid, gas, or solid).
Stabilization: Colloids are stabilized by electrostatic repulsion among the charged layers surrounding individual particles, preventing them from coalescing.
Coagulation: Colloids can be destroyed (coagulated) through processes such as heating or the addition of electrolytes, leading to the aggregation of particles.

''',

'''

Chemical Kinetics
Definition: The study of the factors that control the rate (speed) of a chemical reaction.
Rate Definition: The rate of a reaction is defined in terms of the change in concentration of a given reaction component per unit time.
Kinetic Measurements: Often conducted under conditions where the reverse reaction is insignificant, allowing for simpler analysis.
Relationship to Thermodynamics: The kinetic and thermodynamic properties of a reaction are not fundamentally related; they provide different information about the reaction.
Rate Laws
Rate Constant (k): A proportionality constant in the rate law that is specific to each reaction and varies with temperature.
Order of Reaction (n): Indicates the power to which the concentration of a reactant is raised in the rate law; it is not necessarily related to the coefficients in the balanced equation.
Integrated Rate Law: Describes how the concentration of reactants changes over time.
Differential Rate Law: Describes the rate of the reaction as a function of the concentration of reactants.
General form:
Rate
=
k
[
A
]
n
Rate=k[A] 
n
 
Special Cases of Integrated Rate Laws

Zero-Order Reaction (
n
=
0
n=0):
Rate Law:
Rate
=
k
[
A
]
0
=
k
Rate=k[A] 
0
 =k
Integrated Form:
[
A
]
=
[
A
]
0
−
k
t
[A]=[A] 
0
​	
 −kt
Half-Life:
t
1
/
2
=
[
A
]
0
2
k
t 
1/2
​	
 = 
2k
[A] 
0
​	
 
​	
 
First-Order Reaction (
n
=
1
n=1):
Rate Law:
Rate
=
k
[
A
]
1
Rate=k[A] 
1
 
Integrated Form:
ln
⁡
[
A
]
=
−
k
t
+
ln
⁡
[
A
]
0
ln[A]=−kt+ln[A] 
0
​	
 
Half-Life:
t
1
/
2
=
0.693
k
t 
1/2
​	
 = 
k
0.693
​	
 
Second-Order Reaction (
n
=
2
n=2):
Rate Law:
Rate
=
k
[
A
]
2
Rate=k[A] 
2
 
Integrated Form:
1
[
A
]
=
k
t
+
1
[
A
]
0
[A]
1
​	
 =kt+ 
[A] 
0
​	
 
1
​	
 
Half-Life:
t
1
/
2
=
1
k
[
A
]
0
t 
1/2
​	
 = 
k[A] 
0
​	
 
1
​	
 
The value of 
k
k can be determined from the plot of the appropriate function of 
[
A
]
[A] versus time.
Reaction Mechanisms
Elementary Steps: A series of individual steps through which an overall reaction occurs. The rate law for each elementary step can be derived from its molecularity.
Requirements for Acceptable Mechanisms:
The elementary steps must sum to give the correct overall balanced equation.
The mechanism must agree with the experimentally determined rate law.
Rate-Determining Step: In a sequence of elementary steps, the slowest step controls the overall rate of the reaction.
Kinetic Models
Collision Model: The simplest model for reaction kinetics, which states that molecules must collide to react.
Collision Energy: The kinetic energy from the collision provides the potential energy necessary for the reactants to rearrange and form products.
Activation Energy (
E
a
E 
a
​	
 ): A threshold energy that must be exceeded for a reaction to occur.
Orientation: The relative orientations of the colliding reactants are critical; certain orientations may be more favorable for reaction.
Arrhenius Equation:
k
=
A
e
−
E
a
/
R
T
k=Ae 
−E 
a
​	
 /RT
 
A
A: The frequency factor, which depends on the collision frequency and the relative orientation of the molecules.
The value of 
E
a
E 
a
​	
  can be determined by measuring 
k
k at different temperatures.
Catalysts
Definition: Substances that speed up a reaction without being consumed in the process.
Mechanism: Catalysts provide an alternative pathway for the reaction with a lower activation energy.
Types of Catalysts:
Homogeneous Catalysts: Exist in the same phase (solid, liquid, gas) as the reactants, facilitating reactions by interacting with them directly.
Heterogeneous Catalysts: Exist in a different phase than the reactants, often solid catalysts in liquid or gas reactions.
Biological Catalysts: Enzymes are specialized catalysts that speed up biochemical reactions.
Acids and Bases: Can also function as catalysts in certain reactions.

''',

'''

Chemical Equilibrium
Definition: When a reaction occurs in a closed system, it eventually reaches a state where the concentrations of reactants and products remain constant over time.
Dynamic State: Although the concentrations are constant, the reactants and products are continually interconverted, meaning that both the forward and reverse reactions are occurring simultaneously.
Forward and Reverse Rates: At equilibrium, the rate of the forward reaction equals the rate of the reverse reaction.
The Law of Mass Action
For the reaction:
j
A
+
k
B
⇌
m
C
+
n
D
jA+kB⇌mC+nD
The equilibrium constant 
K
K is expressed as:
K
=
[
C
]
m
[
D
]
n
[
A
]
j
[
B
]
k
K= 
[A] 
j
 [B] 
k
 
[C] 
m
 [D] 
n
 
​	
 
Exclusion of Pure Substances: Pure liquids and solids are not included in the equilibrium expression.
Equilibrium Constant for Gases: For gas-phase reactions, the equilibrium constant can also be expressed in terms of partial pressures, denoted as 
K
p
K 
p
​	
 :
K
p
=
K
c
(
R
T
)
Δ
n
K 
p
​	
 =K 
c
​	
 (RT) 
Δn
 
where 
Δ
n
Δn is the difference in the sum of the coefficients of gaseous products and reactants, and 
R
R is the universal gas constant.
Equilibrium Position
Definition: A specific set of reactant and product concentrations that satisfies the equilibrium constant expression.
Constant 
K
K: For a given system at a specified temperature, there is one equilibrium constant 
K
K. However, there can be an infinite number of equilibrium positions at that temperature, depending on the initial concentrations.
Magnitude of 
K
K:
A small value of 
K
K indicates that the equilibrium lies to the left (favoring reactants).
A large value of 
K
K indicates that the equilibrium lies to the right (favoring products).
Independence from Reaction Rate: The size of 
K
K does not indicate the speed at which equilibrium is reached.
Reaction Quotient (
Q
Q): Applies the law of mass action to the initial concentrations rather than at equilibrium.
If 
Q
>
K
Q>K, the system will shift to the left (toward reactants) to reach equilibrium.
If 
Q
<
K
Q<K, the system will shift to the right (toward products) to reach equilibrium.
Finding Equilibrium Concentrations:
Start with the initial concentrations (or partial pressures).
Define the changes needed to reach equilibrium.
Apply these changes to the initial concentrations and solve for the equilibrium concentrations.
Le Châtelier’s Principle
Principle Statement: This principle provides a qualitative way to predict how a system at equilibrium will respond to changes in concentration, pressure, and temperature.
Response to Stress: If an external change (stress) is applied to a system at equilibrium, the system will adjust (shift) in a direction that counteracts or relieves the stress.
Types of Stresses:
Change in Concentration: Adding or removing reactants or products will shift the equilibrium position to favor the side that counteracts the change.
Change in Pressure: Increasing pressure favors the side of the reaction with fewer gas molecules, while decreasing pressure favors the side with more gas molecules.
Change in Temperature: For exothermic reactions, increasing temperature shifts the equilibrium to favor reactants (left), while decreasing temperature favors products (right). For endothermic reactions, the reverse is true.

''',

'''

Models for Acids and Bases
1. Arrhenius Model

Definition:
Acids: Substances that produce hydrogen ions (
H
+
H 
+
 ) in solution.
Bases: Substances that produce hydroxide ions (
OH
−
OH 
−
 ) in solution.
2. Brønsted–Lowry Model

Acid: Defined as a proton donor.
Base: Defined as a proton acceptor.
Reaction with Water: An acid reacts with a water molecule (acting as a base):
HA (aq)
+
H
2
O (l)
⇌
H
3
O
+
(
a
q
)
+
A
−
(
a
q
)
HA (aq)+H 
2
​	
 O (l)⇌H 
3
​	
 O 
+
 (aq)+A 
−
 (aq)
This reaction produces a conjugate acid (
H
3
O
+
H 
3
​	
 O 
+
 ) and a conjugate base (
A
−
A 
−
 ).
3. Lewis Model

Lewis Acid: An electron-pair acceptor.
Lewis Base: An electron-pair donor.
Acid–Base Equilibrium
Equilibrium Constant (
K
a
K 
a
​	
 ): The equilibrium constant for an acid dissociating (ionizing) in water is called 
K
a
K 
a
​	
 .
Expression for 
K
a
K 
a
​	
 :
K
a
=
[
H
3
O
+
]
[
A
−
]
[
HA
]
K 
a
​	
 = 
[HA]
[H 
3
​	
 O 
+
 ][A 
−
 ]
​	
 
Simplified as:
K
a
=
[
H
3
O
+
]
[
HA
]
K 
a
​	
 = 
[HA]
[H 
3
​	
 O 
+
 ]
​	
 
Note: The concentration of water 
[
H
2
O
]
[H 
2
​	
 O] is not included as it is assumed to be constant.
Acid Strength
Strong Acids:
Have very large 
K
a
K 
a
​	
  values.
Completely dissociate (ionize) in water.
The dissociation equilibrium position lies far to the right.
Strong acids have very weak conjugate bases.
Common strong acids:
Nitric acid 
[
HNO
3
(
a
q
)
]
[HNO 
3
​	
 (aq)]
Hydrochloric acid 
[
HCl
(
a
q
)
]
[HCl(aq)]
Sulfuric acid 
[
H
2
SO
4
(
a
q
)
]
[H 
2
​	
 SO 
4
​	
 (aq)]
Perchloric acid 
[
HClO
4
(
a
q
)
]
[HClO 
4
​	
 (aq)]
Weak Acids:
Have small 
K
a
K 
a
​	
  values.
Dissociate (ionize) to a slight extent.
The dissociation equilibrium position lies far to the left.
Weak acids have relatively strong conjugate bases.
Percent Dissociation:
Percent Dissociation
=
(
Amount Dissociated (mol/L)
Initial Concentration (mol/L)
)
×
100
%
Percent Dissociation=( 
Initial Concentration (mol/L)
Amount Dissociated (mol/L)
​	
 )×100%
A smaller percent dissociation indicates a weaker acid.
Dilution of a weak acid increases its percent dissociation.
Autoionization of Water
Amphoteric Nature: Water can act as both an acid and a base.
Self-Reaction:
H
2
O (l)
+
H
2
O (l)
⇌
H
3
O
+
(
a
q
)
+
OH
−
(
a
q
)
H 
2
​	
 O (l)+H 
2
​	
 O (l)⇌H 
3
​	
 O 
+
 (aq)+OH 
−
 (aq)
Equilibrium Expression:
K
w
=
[
H
3
O
+
]
[
OH
−
]
K 
w
​	
 =[H 
3
​	
 O 
+
 ][OH 
−
 ]
Ion-Product Constant for Water: At 25°C, 
[
H
+
]
=
[
O
H
−
]
=
1.0
×
10
−
7
[H 
+
 ]=[OH 
−
 ]=1.0×10 
−7
 , so 
K
w
=
1.0
×
10
−
14
K 
w
​	
 =1.0×10 
−14
 .
Solution Classifications:
Acidic Solution: 
[
H
+
]
>
[
O
H
−
]
[H 
+
 ]>[OH 
−
 ]
Basic Solution: 
[
O
H
−
]
>
[
H
+
]
[OH 
−
 ]>[H 
+
 ]
Neutral Solution: 
[
H
+
]
=
[
O
H
−
]
[H 
+
 ]=[OH 
−
 ]
The pH Scale
Definition:
pH
=
−
log
⁡
[
H
+
]
pH=−log[H 
+
 ]
Logarithmic Scale:
pH changes by 1 unit for every 10-fold change in 
[
H
+
]
[H 
+
 ].
Similar log scales apply for 
[
OH
−
]
[OH 
−
 ] and 
K
a
K 
a
​	
 :
pOH
=
−
log
⁡
[
OH
−
]
,
pK
a
=
−
log
⁡
K
a
pOH=−log[OH 
−
 ],pK 
a
​	
 =−logK 
a
​	
 
Bases
Strong Bases: Typically hydroxide salts such as sodium hydroxide 
[
NaOH
]
[NaOH] and potassium hydroxide 
[
KOH
]
[KOH].
Weak Bases: React with water to produce hydroxide ions:
B (aq)
+
H
2
O (l)
⇌
BH
+
(
a
q
)
+
OH
−
(
a
q
)
B (aq)+H 
2
​	
 O (l)⇌BH 
+
 (aq)+OH 
−
 (aq)
Equilibrium Constant for Weak Bases (
K
b
K 
b
​	
 ):
K
b
=
[
BH
+
]
[
OH
−
]
[
B
]
K 
b
​	
 = 
[B]
[BH 
+
 ][OH 
−
 ]
​	
 
In water, a weak base 
B
B is always competing with hydroxide ions for protons, leading to generally small 
K
b
K 
b
​	
  values.

Polyprotic Acids
Definition: A polyprotic acid is an acid that can donate more than one proton (
H
+
H 
+
 ) per molecule.
Dissociation Process:
Polyprotic acids dissociate one proton at a time through multiple ionization steps.
Characteristic 
K
a
K 
a
​	
  Values:
Each step of dissociation has a specific equilibrium constant, denoted as 
K
a
1
K 
a1
​	
 , 
K
a
2
K 
a2
​	
 , etc.
Typically, for a weak polyprotic acid:
K
a
1
>
K
a
2
>
K
a
3
K 
a1
​	
 >K 
a2
​	
 >K 
a3
​	
 
Unique Case of Sulfuric Acid:
Sulfuric acid (
H
2
SO
4
H 
2
​	
 SO 
4
​	
 ) is notable because:
The first dissociation step is strong (
K
a
1
K 
a1
​	
  is very large), leading to complete ionization.
The second dissociation step is weak, characterized by a smaller 
K
a
2
K 
a2
​	
 .
Acid–Base Properties of Salts
Solution Types: Salts can produce acidic, basic, or neutral solutions in water based on their constituent ions.
Neutral Solutions:
Formed by salts that contain:
Cations from strong bases and anions from strong acids.
Basic Solutions:
Formed by salts that contain:
Cations from strong bases and anions from weak acids.
Acidic Solutions:
Formed by salts that contain:
Cations from weak bases and anions from strong acids.
Also produced by salts containing highly charged metal cations, such as:
Al
3
+
Al 
3+
  and 
Fe
3
+
Fe 
3+
 .
Effect of Structure on Acid–Base Properties
Functional Group: Many substances that act as acids or bases contain the 
HOOX
HOOX grouping, where 
X
X represents another atom or group.
Acid Behavior:
Molecules with a strong and covalent 
OX
OX bond tend to exhibit acidic behavior, effectively donating protons.
As the electronegativity of 
X
X increases, the strength of the acid generally increases.
Base Behavior:
When the 
OX
OX bond is more ionic, the substance tends to behave as a base, releasing hydroxide ions (
OH
−
OH 
−
 ) when dissolved in water.

''',

'''

Buffered Solutions
Definition: A buffered solution contains either a weak acid (
HA
HA) and its salt (e.g., 
NaA
NaA) or a weak base (
B
B) and its salt (e.g., 
BHCl
BHCl).
Function: Buffered solutions resist changes in pH when small amounts of 
H
+
H 
+
  or 
OH
−
OH 
−
  are added.
Henderson–Hasselbalch Equation:
For a buffered solution containing 
HA
HA and its conjugate base 
A
−
A 
−
 , the pH can be calculated using the Henderson–Hasselbalch equation:
pH
=
p
K
a
+
log
⁡
(
[
A
−
]
[
HA
]
)
pH=pK 
a
​	
 +log( 
[HA]
[A 
−
 ]
​	
 )
Buffer Capacity:
The capacity of the buffered solution depends on the concentrations of 
HA
HA and 
A
−
A 
−
 present.
The most efficient buffering occurs when the ratio of 
[
HA
]
[HA] to 
[
A
−
]
[A 
−
 ] is close to 1.
Mechanism of Buffering:
Buffering works because the amounts of 
HA
HA (which reacts with added 
OH
−
OH 
−
 ) and 
A
−
A 
−
 (which reacts with added 
H
+
H 
+
 ) are large enough to maintain the 
[
HA
]
[HA] to 
[
A
−
]
[A 
−
 ] ratio, preventing significant changes in pH upon the addition of strong acids or bases.
Acid-Base Titrations
Titration Process:
The progress of a titration is represented by plotting the pH of the solution versus the volume of added titrant. The resulting graph is called a pH curve or titration curve.
Strong Acid–Strong Base Titrations:
These titrations exhibit a sharp change in pH near the equivalence point, where stoichiometric amounts of acid and base have reacted.
Titration Curve Shapes:
The shape of the pH curve for a strong base–weak acid titration differs significantly from that of a strong acid–strong base titration.
For a strong base–weak acid titration, the pH at the equivalence point is greater than 7 due to the basic properties of the conjugate base 
A
−
A 
−
 .
Indicators:
Indicators are substances used to mark the equivalence point of an acid-base titration.
The end point of the titration is where the indicator changes color.
The goal is to have the end point and the equivalence point coincide as closely as possible to ensure accurate titration results.

''',

'''

Solids Dissolving in Water
Slightly Soluble Salts:
For a slightly soluble salt (e.g., 
MX
MX), an equilibrium is established between the excess solid and the ions in solution:
MX (s)
⇌
M
+
(
a
q
)
+
X
−
(
a
q
)
MX (s)⇌M 
+
 (aq)+X 
−
 (aq)
Solubility Product Constant (
K
s
p
K 
sp
​	
 ):
The corresponding equilibrium constant for this dissolution is known as the solubility product constant (
K
s
p
K 
sp
​	
 ):
K
s
p
=
[
M
+
]
[
X
−
]
K 
sp
​	
 =[M 
+
 ][X 
−
 ]
Common Ion Effect:
The solubility of 
MX
(
s
)
MX(s) is decreased by the presence of another source of either 
M
+
M 
+
  or
X
−
X 
−
 . This phenomenon is referred to as the common ion effect.
Predicting Precipitation:
To determine whether precipitation will occur when two solutions are mixed, calculate the reaction quotient (
Q
Q) for the initial concentrations:
If 
Q
>
K
s
p
Q>K 
sp
​	
 , precipitation occurs.
If 
Q
≤
K
s
p
Q≤K 
sp
​	
 , no precipitation occurs.
Qualitative Analysis
Selective Precipitation:
A mixture of ions can be separated through selective precipitation, which involves the following steps:
Group Separation:
Ions are first grouped by adding hydrochloric acid (
HCl (aq)
HCl (aq)), followed by hydrogen sulfide (
H
2
S (aq)
H 
2
​	
 S (aq)), sodium hydroxide (
NaOH (aq)
NaOH (aq)), and sodium carbonate (
Na
2
CO
3
(
a
q
)
Na 
2
​	
 CO 
3
​	
 (aq)).
Identification:
The ions in each group are then further separated and identified using additional selective dissolution and precipitation methods.
Complex Ions
Definition:
Complex ions are formed from a metal ion surrounded by attached ligands.
Ligands:
A ligand is a Lewis base that donates a pair of electrons to the metal ion.
Coordination Number:
The number of ligands attached to the metal ion is known as the coordination number, which is typically 2, 4, or 6.
Equilibria in Solution:
Complex ion equilibria in solution are described by formation (stability) constants, indicating the stability of the complex ion.
Application in Qualitative Analysis:
The formation of complex ions can be utilized to selectively dissolve solids within the qualitative analysis framework, aiding in the separation and identification of ions.

''',

'''

First Law of Thermodynamics
Energy Conservation:
The first law states that the energy of the universe is constant. It emphasizes that energy cannot be created or destroyed, only transformed from one form to another.
Energy Tracking:
This law provides a framework to keep track of energy changes as they occur in various processes.
Direction of Processes:
It does not provide information regarding why a particular process occurs in a specific direction.
Second Law of Thermodynamics
Entropy and Spontaneous Processes:
The second law states that for any spontaneous (thermodynamically favored) process, there is always an increase in the entropy of the universe.
Entropy (
S
S):
Entropy is a thermodynamic function that quantifies the number of arrangements (positions and/or energy levels) available to a system in a given state.
Natural Progression:
Nature tends to spontaneously move toward states with the highest probability of occurring, indicating a preference for disorder or higher entropy.
Predicting Direction:
Using entropy, thermodynamics can predict the direction in which a process will spontaneously occur:
Δ
S
u
n
i
v
=
Δ
S
s
y
s
+
Δ
S
s
u
r
r
ΔS 
univ
​	
 =ΔS 
sys
​	
 +ΔS 
surr
​	
 
For a spontaneous process, 
Δ
S
u
n
i
v
ΔS 
univ
​	
  must be positive.
Entropy Contributions:
At constant temperature and pressure:
Δ
S
s
y
s
ΔS 
sys
​	
  is primarily influenced by “positional” entropy.
For chemical reactions, 
Δ
S
s
y
s
ΔS 
sys
​	
  is dominated by changes in the number of gaseous molecules.
Surroundings and Heat:
Δ
S
s
u
r
r
ΔS 
surr
​	
  is determined by heat:
Δ
S
s
u
r
r
=
−
Δ
H
T
ΔS 
surr
​	
 =− 
T
ΔH
​	
 
Δ
S
s
u
r
r
ΔS 
surr
​	
  is positive for exothermic processes (where 
Δ
H
ΔH is negative).
Temperature Dependency:
Since 
Δ
S
s
u
r
r
ΔS 
surr
​	
  depends inversely on temperature, exothermicity becomes a more significant driving force at lower temperatures.
Rate of Processes:
Thermodynamics cannot predict the rate at which a system will spontaneously change; principles of kinetics are required for that.
Third Law of Thermodynamics
Entropy at Absolute Zero:
The third law states that the entropy of a perfect crystal at absolute zero (0 K) is zero, indicating that there is only one microstate available at this temperature.
Free Energy (
G
G)
Definition and Spontaneity:
Free energy is a state function that indicates the spontaneity of processes at constant temperature and pressure:
G
=
H
−
T
S
G=H−TS
A process is spontaneous in the direction in which its free energy decreases (
Δ
G
<
0
ΔG<0).
Standard Free Energy Change:
The standard free energy change (
Δ
G
∘
ΔG 
∘
 ) is the change in free energy that occurs when reactants in their standard states are converted to products in their standard states.
Calculating Standard Free Energy Change:
The standard free energy change for a reaction can be calculated from the standard free energies of formation (
Δ
G
f
∘
ΔG 
f
∘
​	
 ):
Δ
G
∘
=
∑
Δ
G
p
r
o
d
u
c
t
s
∘
−
∑
Δ
G
r
e
a
c
t
a
n
t
s
∘
ΔG 
∘
 =∑ΔG 
products
∘
​	
 −∑ΔG 
reactants
∘
​	
 
Temperature and Pressure Dependence:
Free energy also depends on temperature and pressure:
G
=
G
∘
+
R
T
ln
⁡
P
G=G 
∘
 +RTlnP
Relationship with Equilibrium Constant:
This relationship allows for the derivation of the connection between 
Δ
G
∘
ΔG 
∘
  for a reaction and its equilibrium constant (
K
K):
Δ
G
∘
=
−
R
T
ln
⁡
K
ΔG 
∘
 =−RTlnK
Where:
Δ
G
∘
=
0
ΔG 
∘
 =0 implies 
K
=
1
K=1
Δ
G
∘
<
0
ΔG 
∘
 <0 implies 
K
>
1
K>1
Δ
G
∘
>
0
ΔG 
∘
 >0 implies 
K
<
1
K<1
Maximum Work:
The maximum possible useful work obtainable from a process at constant temperature and pressure is equal to the change in free energy:
w
m
a
x
=
Δ
G
w 
max
​	
 =ΔG
Energy Use in Real Processes:
When energy is utilized to do work in a real process, the total energy of the universe remains constant, but the usefulness of that energy diminishes.
Energy Distribution:
Concentrated energy disperses in the surroundings as thermal energy.

''',

'''



'''

]

bio_text = [

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 2.1
Matter consists of chemical elements in pure form and in combinations called compounds (pp. 29-30)
■ Elements cannot be broken down chemically
to other substances. A compound contains two
VOCAB SELF-QUIZ goo.gl/6u55ks
or more different elements in a fixed ratio. Oxygen, carbon, hydrogen, and nitrogen make up approximately 96% of living matter.
? Compare an element and a compound.
CONCEPT 2.2
An element's properties depend on the structure of its atoms (pp. 30-36)
An atom, the smallest unit of an element, has the following components:
Nucleus
Protons (+ charge)- determine element
Neutrons (no charge)- determine isotope
Atom
Electrons (charge) form negative cloud and determine chemical behavior
■ An electrically neutral atom has equal numbers of electrons and protons; the number of protons determines the atomic number. The atomic mass is measured in daltons and is roughly equal to the mass number, the sum of protons plus neutrons. Isotopes of an element differ from each other in neutron number and therefore mass. Unstable isotopes give off particles and energy as radioactivity.
■ In an atom, electrons occupy specific electron shells; the elec- trons in a shell have a characteristic energy level. Electron distri- bution in shells determines the chemical behavior of an atom. An atom that has an incomplete outer shell, the valence shell, is reactive.
■ Electrons exist in orbitals, three-dimensional spaces with spe- cific shapes that are components of electron shells.
Molecules consist of two or more covalently bonded atoms. The attraction of an atom for the electrons of a covalent bond is its electronegativity. If both atoms are the same, they have the same electronegativity and share a nonpolar covalent bond. Electrons of a polar covalent bond are pulled closer to the more electronegative atom, such as the oxygen in H2O. An ion forms when an atom or molecule gains or loses an elec- tron and becomes charged. An ionic bond is the attraction between two oppositely charged ions:
(Na)
Na Sodium atom
CI Chlorine atom
Electron transfer forms ions
Na
Ionic bond
Na+ Sodium ion (a cation)
CI
Chloride ion
(an anion)
Weak interactions reinforce the shapes of large molecules and help molecules adhere to each other. A hydrogen bond is an attraction between a hydrogen atom carrying a partial positive charge (8+) and an electronegative atom carrying a partial nega- tive charge (8-). Van der Waals interactions occur between transiently positive and negative regions of molecules.
■ A molecule's shape is determined by the positions of its atoms' valence orbitals. Covalent bonds result in hybrid orbitals, which are responsible for the shapes of H2O, CH1, and many more com- plex biological molecules. Molecular shape is usually the basis for the recognition of one biological molecule by another.
? In terms of electron sharing between atoms, compare nonpolar covalent bonds, polar covalent bonds, and the formation of ions.
CONCEPT 2.4
Chemical reactions make and break chemical bonds (pp. 40-41)
■Chemical reactions change reactants into products while conserving matter. All chemical reactions are theoretically revers- ible. Chemical equilibrium is reached when the forward and reverse reaction rates are equal.

CONCEPT 2.3
The formation and function of molecules depend on chemical bonding between atoms (pp. 36-40)
Chemical bonds form when atoms interact and complete their valence shells. Covalent bonds form when pairs of electrons are shared:
H. + H.
H:H Single
0 +0:
0::0
Double
covalent bond
covalent bond

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 3.1
Polar covalent bonds in water
molecules result in hydrogen
bonding (p. 45)
■Water is a polar molecule. A hydrogen bond
forms when a partially negatively charged region on the oxygen of one
water molecule is attracted to the
partially positively charged hydro-
8+8
gen of a nearby water molecule. Hydrogen bonding between water molecules is the
basis for water's properties.
VOCAB
SELF-QUIZ goo.gl/6u55ks
st...8
DRAW IT ➤ Label a hydrogen bond and a polar covalent bond in the dia- gram of five water molecules. Is a hydrogen bond a covalent bond? Explain.
CONCEPT 3.2
Four emergent properties of water contribute to Earth's suitability for life (pp. 45-50)
■ Hydrogen bonding keeps water molecules close to each other, giving water cohesion. Hydrogen bonding is also responsible for water's surface tension.
■Water has a high specific heat: Heat is absorbed when hydrogen bonds break and is released when hydrogen bonds form. This helps keep temperatures relatively steady, within limits that permit life. Evaporative cooling is based on water's high heat of vaporization. The evaporative loss of the most energetic water molecules cools a surface.

■ Ice floats because it is less dense than liquid water. This property allows life to exist under the frozen surfaces of lakes and polar seas. ■Water is an unusually versatile solvent because its polar mol- ecules are attracted to ions and polar substances that can form hydrogen bonds. Hydrophilic substances have an affinity for water; hydrophobic substances do not. Molarity, the number of moles of solute per liter of solution, is used as a measure of solute concentration in solutions. A mole is a certain number of molecules of a substance. The mass of a mole of a substance in grams is the same as the molecular mass in daltons. The emergent properties of water support life on Earth and may contribute to the potential for life to have evolved on other planets.

CONCEPT 3.3
Acidic and basic conditions affect living
organisms (pp. 51-54)
■ A water molecule can transfer an H+ to another water molecule
0
Acidic [H+] > [OH]
Acids donate H+ in aqueous solutions.
to form H3O+ (represented simply by H*) and OH. ■The concentration of H+ is expressed as pH; pH = −log [H+]. A buffer consists of an acid-base pair that combines reversibly with hydrogen ions, allowing it to resist pH changes. ■The burning of fossil fuels increases the amount of CO2 in the atmosphere. Some CO2 dissolves in the oceans, causing ocean acidification, which has potentially grave conse- quences for marine organisms that rely on calcification.
Neutral [H+] = [OH]
-7
Bases donate OH or accept H* in aqueous solutions.
Basic [H+] < [OH]
-14

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 4.1
Organic chemistry is the study of carbon compounds (pp. 57-58)
■ Organic compounds, once thought to arise only within living organisms, were finally synthesized in the laboratory.
VOCAB SELF-QUIZ goo.gl/6u55ks
■Living matter is made mostly of carbon, oxygen, hydrogen, and nitrogen. Biological diversity results from carbon's ability to form a huge number of molecules with particular shapes and properties. ? How did Stanley Miller's experiments support the idea that, even at life's origins, physical and chemical laws govern the processes of life?
CONCEPT 4.2
Carbon atoms can form diverse molecules by bonding to four other atoms (pp. 58-62)
Carbon, with a valence of 4, can bond to various other atoms, including O, H, and N. Carbon can also bond to other carbon
atoms, forming the carbon skeletons of organic compounds. These skeletons vary in length and shape and have bonding sites for atoms of other elements.
■ Hydrocarbons consist of carbon and hydrogen.
■ Isomers are compounds that have the same molecular formula but different structures and therefore different properties. Three types of isomers are structural isomers, cis-trans isomers, and enantiomers.
VISUAL SKILLS > Refer back to Figure 4.9. What type of isomers are acetone and propanal? How many asymmetric carbons are present in acetic acid, glycine, and glycerol phosphate? Can these three molecules exist as forms that are enantiomers?
CONCEPT 4.3
A few chemical groups are key to molecular function (pp. 62-64)
Chemical groups attached to the carbon skeletons of organic molecules participate in chemical reactions (functional groups) or contribute to function by affecting molecular shape (see Figure 4.9).
■ ATP (adenosine triphosphate) consists of adenosine attached to three phosphate groups. ATP can react with water, forming

ADP (adenosine diphosphate) and inorganic phosphate. This reaction releases energy that can be used by the cell.
Reacts with H2O
Adenosine
Adenosine + P+ Energy
ATP
ADP
Inorganic
phosphate

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 5.1
Macromolecules are polymers, built from monomers (pp. 67-68)
■Large carbohydrates (polysaccharides), proteins, and nucleic acids are polymers, which are chains
Large Biological Molecules
CONCEPT 5.2
Carbohydrates serve as
fuel and building material (pp. 68-72)
? Compare the composition, structure, and
function of starch and cellulose. What role do starch and cellulose play in the human body?
CONCEPT 5.3
Lipids are a diverse group of hydrophobic molecules (pp. 72-75)
? Why are lipids not considered to be polymers or macromolecules?
VOCAB
SELF-QUIZ goo.gl/6u55ks
Components
of monomers. The components of lipids vary. Monomers form larger molecules by dehydration reactions, in which water molecules are released. Polymers can disassemble by the reverse process, hydrolysis. An immense variety of polymers can be built from a small set of monomers.
? What is the fundamental basis for the differences between large carbohydrates, proteins, and nucleic acids?
Examples
Monosaccharides: glucose,
CH2OH
fructose
H
H
OH H
HO
OH
H OH
Monosaccharide monomer
Glycerol
> 3 fatty acids
-Head with P
2 fatty acids.
Disaccharides: lactose, sucrose
Polysaccharides:
■ Cellulose (plants) ■ Starch (plants)
■ Glycogen (animals)
■ Chitin (animals and fungi)
Triacylglycerols (fats or oils): glycerol + three fatty acids
Phospholipids: glycerol + phosphate group + two fatty acids
Functions
Fuel; carbon sources that can be converted to other molecules or combined into polymers
■ Strengthens plant cell walls ■ Stores glucose for energy ■ Stores glucose for energy
■ Strengthens exoskeletons and fungal cell walls Important energy source
Lipid bilayers of membranes
Hydrophobic tails
Hydrophilic
CONCEPT 5.4
Proteins include a diversity of structures, resulting in a wide range of functions (pp. 75-83)
? Explain the basis for the great diversity of proteins.
CONCEPT 5.5
Nucleic acids store, transmit, and help express hereditary information (pp. 84-86)
What role does complementary base pairing play in the functions of nucleic acids?
Steroids: four fused rings with attached chemical groups
Steroid backbone
■ Enzymes
R
■ Defensive proteins
■ Storage proteins
■ Transport proteins
■ Hormones
OH
H
■ Receptor proteins
Amino acid monomer (20 types)
■ Motor proteins
■ Structural proteins
Nitrogenous base
DNA:
Phosphate group
PCH2 Q Sugar
Nucleotide (monomer of a polynucleotide)
heads
■Component of cell membranes (cholesterol)
Signaling molecules that travel through the body (hormones)
■ Catalyze chemical reactions
■ Protect against disease
■ Store amino acids
■ Transport substances
■ Coordinate organismal responses
■ Receive signals from outside cell
■ Function in cell movement
■ Provide structural support
Xx Stores hereditary information
■ Sugar = deoxyribose Nitrogenous bases = C, G, A, T Usually double-stranded
RNA:
■ Sugar = ribose
■ Nitrogenous bases C, G, A, U ■ Usually single-stranded
Various functions in gene expression, including carrying instructions from DNA to ribosomes

CONCEPT 5.6
Genomics and proteomics have transformed biological inquiry and applications (pp. 86-89)
■ Recent technological advances in DNA sequencing have given rise to genomics, an approach that analyzes large sets of genes or whole genomes, and proteomics, a similar approach for large sets of proteins. Bioinformatics is the use of computational tools and computer software to analyze these large data sets. ■The more closely two species are related evolutionarily, the more similar their DNA sequences are. DNA sequence data confirm models of evolution based on fossils and anatomical evidence.

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 6.1
Biologists use microscopes and biochemistry to study cells (pp. 94-97)
VOCAB SELF-QUIZ goo.gl/6u55ks
Improvements in microscopy that affect the param- eters of magnification, resolution, and contrast have catalyzed progress in the study of cell structure. Light microscopy (LM) and electron microscopy (EM), as well as other types, remain important tools.
■ Cell biologists can obtain pellets enriched in particular cellular components by centrifuging disrupted cells at sequential speeds, a process known as cell fractionation.
? How do microscopy and biochemistry complement each other to reveal
cell structure and function?
CONCEPT 6.2
Eukaryotic cells have internal membranes that compartmentalize their functions (pp. 97-102)
■ All cells are bounded by a plasma membrane.
■ Prokaryotic cells lack nuclei and other membrane-enclosed organelles, while eukaryotic cells have internal membranes that compartmentalize cellular functions.
■The surface-to-volume ratio is an important parameter affecting cell size and shape.
■ Plant and animal cells have most of the same organelles: a nucleus, endoplasmic reticulum, Golgi apparatus, and mitochondria. Chloroplasts are present only in cells of photosynthetic eukaryotes.
? Explain how the compartmental organization of a eukaryotic cell contributes to its biochemical functioning.
CONCEPT 6.3
The eukaryotic cell's genetic instructions are housed in the nucleus and carried out by the ribosomes (pp. 102-104) ? Describe the relationship
between the nucleus and ribosomes.
CONCEPT 6.4
The endomembrane system regulates protein traffic and performs metabolic functions (pp. 104-109)
? Describe the key role played by transport vesicles in the endomembrane system.
Cell Component
Nucleus
Structure
Surrounded by nuclear envelope (double membrane) perforated by nuclear pores; nuclear envelope continuous with endoplasmic reticulum (ER)
Function
Houses chromosomes, which are made of chromatin (DNA and pro- teins); contains nucleoli, where ribosomal subunits are made; pores regulate entry and exit of materials
(ER)
Ribosome
Endoplasmic reticulum (ER)
Golgi apparatus
Lysosome
Vacuole
(Nuclear envelope)
Two subunits made of ribosomal RNAs and proteins; can be free in cytosol or bound to ER
Extensive network of membrane- bounded tubules and sacs; mem- brane separates lumen from cytosol; continuous with nuclear envelope
Stacks of flattened membranous sacs; has polarity (cis and trans faces)
Membranous sac of hydrolytic enzymes (in animal cells)
Protein synthesis
Smooth ER: synthesis of lipids, metabolism of carbohydrates, Ca2+ storage, detoxification of drugs and poisons
Rough ER: aids in synthesis of secre- tory and other proteins on bound ribosomes; adds carbohydrates to proteins to make glycoproteins; produces new membrane
Modification of proteins, carbohydrates on proteins, and phospholipids; synthesis of many polysaccharides; sorting of Golgi products, which are then released in vesicles
Breakdown of ingested substances, cell macromolecules, and damaged organelles for recycling
Large membrane-bounded vesicle Digestion, storage, waste disposal, water balance, cell growth, and
protection

CONCEPT 6.5 Mitochondria and chloroplasts change energy from one form to another (pp. 109-112)
? What does the endosymbiont theory propose as the origin for mitochondria and chloroplasts? Explain.
Cell Component
Mitochondrion
Chloroplast
Peroxisome
www
Structure
Bounded by double membrane; inner membrane has infoldings
Typically two membranes around fluid stroma, which contains thylakoids stacked into grana
Specialized metabolic compartment bounded by a single membrane
Function
Cellular respiration
Photosynthesis (chloroplasts are in cells of photosynthetic eukaryotes, including plants)
Contains enzymes that transfer H atoms from substrates to oxygen, producing H2O2 (hydrogen peroxide), which is converted to H2O.

CONCEPT 6.6
The cytoskeleton is a network of fibers that organizes structures and activities in the cell (pp. 112-118)
■ The cytoskeleton functions in structural support for the cell and in motility and signal transmission.
■ Microtubules shape the cell, guide organelle movement, and sep- arate chromosomes in dividing cells. Cilia and flagella are motile appendages containing microtubules. Primary cilia also play sen- sory and signaling roles. Microfilaments are thin rods that func- tion in muscle contraction, amoeboid movement, cytoplasmic streaming, and support of microvilli. Intermediate filaments support cell shape and fix organelles in place.
? Describe the role of motor proteins inside the eukaryotic cell and
in whole-cell movement.
CONCEPT 6.7
Extracellular components and connections between cells help coordinate cellular activities (pp. 118–121)
■ Plant cell walls are made of cellulose fibers embedded in other polysaccharides and proteins.
■ Animal cells secrete glycoproteins and proteoglycans that form the extracellular matrix (ECM), which functions in support, adhesion, movement, and regulation.
■ Cell junctions connect neighboring cells. Plants have plasmo- desmata that pass through adjoining cell walls. Animal cells have tight junctions, desmosomes, and gap junctions.

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 7.1
Cellular membranes are fluid mosaics
of lipids and proteins (pp. 127-131)
■ In the fluid mosaic model, amphipathic proteins
are embedded in the phospholipid bilayer.
■ Phospholipids and some proteins move sideways
VOCAB SELF-QUIZ goo.gl/6u55ks
within the membrane. The unsaturated hydrocarbon tails of some phospholipids keep membranes fluid at lower temperatures, while cholesterol helps membranes resist changes in fluidity caused by temperature changes.
■ Membrane proteins function in transport, enzymatic activity, sig- nal transduction, cell-cell recognition, intercellular joining, and attachment to the cytoskeleton and extracellular matrix. Short chains of sugars linked to proteins (in glycoproteins) and lipids (in glycolipids) on the exterior side of the plasma membrane interact with surface molecules of other cells.
■ Membrane proteins and lipids are synthesized in the ER and modified in the ER and Golgi apparatus. The inside and outside faces of membranes differ in molecular composition.
? In what ways are membranes crucial to life?
CONCEPT 7.2
Membrane structure results in selective permeability (pp. 131-132)
■ A cell must exchange molecules and ions with its surroundings, a process controlled by the selective permeability of the plasma membrane. Hydrophobic substances are soluble in lipids and pass through membranes rapidly, whereas polar molecules and ions generally require specific transport proteins.
? How do aquaporins affect the permeability of a membrane?
CONCEPT 7.3
Passive transport is diffusion of a substance across a membrane with no energy investment (pp. 132-136)
■ Diffusion is the spontaneous movement of a substance down its concentration gradient. Water diffuses out through the per- meable membrane of a cell (osmosis) if the solution outside has
a higher solute concentration (hypertonic) than the cytosol; water enters the cell if the solution has a lower solute concentra- tion (hypotonic). If the concentrations are equal (isotonic), no net osmosis occurs. Cell survival depends on balancing water uptake and loss. ■In facilitated
diffusion, a transport protein speeds the movement of water or a solute across a mem- brane down its concen- tration gradient. Ion channels facilitate the diffusion of ions across a membrane. Carrier proteins can undergo changes in shape that translocate bound solutes across the membrane.
Passive transport: Facilitated diffusion
Channel protein
-Carrier protein
? What happens to a cell placed in a hypertonic solution? Describe the free water concentration inside and out.
CONCEPT 7.4
Active transport uses energy to move solutes against their gradients
(pp. 136-139)
■ Specific membrane proteins use energy, usually in the form of ATP, to do the work of active transport.
■Ions can have both a concentration (chemical) gradient and an electrical gra- dient (voltage). These gradients combine in the electrochemical gradient, which determines the net direction of ionic diffusion.
■ Cotransport of two solutes occurs when a membrane protein enables the "downhill" diffusion of one solute to drive the "uphill" transport of the other.
Active transport
ATP
? ATP is not directly involved in the functioning of a cotransporter. Why, then, is cotransport considered active transport?

CONCEPT 7.5
Bulk transport across the plasma membrane
occurs by exocytosis and endocytosis (pp. 139–141)
■In exocytosis, transport vesicles migrate to the plasma membrane, fuse with it, and release their contents. In endocytosis, molecules enter cells within vesicles that pinch inward from the plasma membrane. The three types of endocytosis are phagocytosis, pinocytosis, and receptor-mediated endocytosis.

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 8.1
An organism's metabolism transforms matter and energy, subject to the laws of thermodynamics (pp. 144-147)
VOCAB SELF-QUIZ goo.gl/6u55ks
■ Metabolism is the collection of chemical reactions that occur in an organism. Enzymes catalyze reactions in intersecting metabolic pathways, which may be catabolic (breaking down molecules, releasing energy) or anabolic (building molecules, consuming energy). Bioenergetics is the study of the flow of energy through living organisms.
■ Energy is the capacity to cause change; some forms of energy do work by moving matter. Kinetic energy is associated with motion and includes thermal energy associated with random motion of atoms or molecules. Heat is thermal energy in transfer from one object to another. Potential energy is related to the location or structure of matter and includes chemical energy possessed by a molecule due to its structure.
The first law of thermodynamics, conservation of energy, states that energy cannot be created or destroyed, only transferred or transformed. The second law of thermodynamics states that spontaneous processes, those requiring no outside input of energy, increase the entropy (molecular disorder) of the universe.
? Explain how the highly ordered structure of a cell does not conflict with the second law of thermodynamics.
CONCEPT 8.2
The free-energy change of a reaction tells us whether or not the reaction occurs spontaneously (pp. 147-150)
■ A living system's free energy is energy that can do work under cellular conditions. The change in free energy (AG) during a bio- logical process is related directly to enthalpy change (AH) and to the change in entropy (AS): AG=AH-TAS. Organisms live at the expense of free energy. A spontaneous process occurs with no energy input; during such a process, free energy decreases and the stability of a system increases. At maximum stability, the system is at equilibrium and can do no work.
■ In an exergonic (spontaneous) chemical reaction, the products have less free energy than the reactants (-AG). Endergonic (nonspontaneous) reactions require an input of energy (+AG). The addition of starting materials and the removal of end prod- ucts prevent metabolism from reaching equilibrium.
? Explain the meaning of each component in the equation for the change in free energy of a spontaneous chemical reaction. Why are spontaneous reactions important in the metabolism of a cell?
CONCEPT 8.3
ATP powers cellular work by coupling exergonic reactions to endergonic reactions (pp. 150-153)
■ ATP is the cell's energy shuttle. Hydrolysis of its terminal phos- phate yields ADP and D, and releases free energy.
■ Through energy coupling, the exergonic process of ATP hydro- lysis drives endergonic reactions by transfer of a phosphate group to specific reactants, forming a phosphorylated intermediate
that is more reactive. ATP hydrolysis (sometimes with protein phosphorylation) also causes changes in the shape and binding affinities of transport and motor proteins.
■ Catabolic pathways drive regeneration of ATP from ADP+℗1. ? Describe the ATP cycle: How is ATP used and regenerated in a cell? CONCEPT 8.4
Enzymes speed up metabolic reactions
by lowering energy barriers (pp. 153-159)
In a chemical reaction, the energy necessary to break the bonds of the reactants is the activation energy, EA.
■ Enzymes lower the E, barrier:
-
Free energy
Course of reaction
without
enzyme
EA
without enzyme
EA with enzyme is lower
Reactants
Course of reaction
with enzyme
AG is unaffected by enzyme
Progress of the reaction
Products
Each enzyme has a unique active site that binds one or more substrate(s), the reactants on which it acts. It then changes shape, binding the substrate(s) more tightly (induced fit). ■ The active site can lower an E, barrier by orienting substrates correctly, straining their bonds, providing a favorable micro- environment, or even covalently bonding with the substrate. Each enzyme has an optimal temperature and pH. Inhibitors reduce enzyme function. A competitive inhibitor binds to the active site, whereas a noncompetitive inhibitor binds to a different site on the enzyme.
■ Natural selection, acting on organisms with variant enzymes, is responsible for the diversity of enzymes found in organisms. ? How do both activation energy barriers and enzymes help maintain the
structural and metabolic order of life?
CONCEPT 8.5
Regulation of enzyme activity helps control metabolism (pp. 159-161)
■Many enzymes are subject to allosteric regulation: Regulatory molecules, either activators or inhibitors, bind to specific regula- tory sites, affecting the shape and function of the enzyme. In cooperativity, binding of one substrate molecule can stimulate binding or activity at other active sites. In feedback inhibition, the end product of a metabolic pathway allosterically inhibits the enzyme for a previous step in the pathway.
Some enzymes are grouped into complexes, some are incorporated into membranes, and some are contained inside organelles, increas- ing the efficiency of metabolic processes.
? What roles do allosteric regulation and feedback inhibition play in the metabolism of a cell?

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 9.1
Catabolic pathways yield energy by oxidizing organic fuels (pp. 165-169)
VOCAB SELF-QUIZ goo.gl/6u55ks
■Cells break down glucose and other organic fuels to yield chemical energy in the form of ATP. Fermentation is a process that results in the partial degradation of glucose without the use of oxygen. The process of cellular respiration is a more complete breakdown of glucose. In aerobic respiration, oxygen is used as a reactant; in anaerobic respiration, other substances are used as reactants in a similar process that harvests chemical energy without oxygen. The cell taps the energy stored in food molecules through redox reactions, in which one substance partially or totally shifts elec- trons to another. Oxidation is the total or partial loss of electrons, while reduction is the total or partial addition of electrons. During aerobic respiration, glucose (C6H12O6) is oxidized to CO2, and O2 is reduced to H2O:
- becomes oxidized-
C6H12O6+ 602 →6 CO2+ 6H2O + Energy - becomes reduced-
■ Electrons lose potential energy during their transfer from glucose or other organic compounds to oxygen. Electrons are usually
passed first to NAD, reducing it to NADH, and are then passed from NADH to an electron transport chain, which conducts the electrons to O, in energy-releasing steps. The energy that is released is used to make ATP.
■ Aerobic respiration occurs in three stages: (1) glycolysis, (2) pyruvate oxidation and the citric acid cycle, and (3) oxidative phosphorylation (electron transport and chemiosmosis).
? Describe the difference between the two processes in cellular respiration that produce ATP: oxidative phosphorylation and substrate-level phosphorylation.
CONCEPT 9.2
Glycolysis harvests chemical energy by oxidizing glucose to pyruvate (pp. 170-171)
■ Glycolysis ("splitting of sugar") is a series of reactions that breaks down glucose into two pyruvate molecules, which may go on to enter the citric acid cycle, and nets 2 ATP and 2 NADH per glucose molecule. Inputs Outputs
GLYCOLYSIS
Glucose
2 Pyruvate + 2 ATP
+ 2 NADH
? Which reactions in glycolysis are the source of energy for the formation of ATP and NADH?

CONCEPT 9.3
After pyruvate is oxidized, the citric acid cycle completes the energy-yielding oxidation of organic molecules (pp. 171-174)
■In eukaryotic cells, pyruvate enters the mitochondrion and is oxidized to acetyl CoA, which is further oxidized in the citric acid cycle.
Outputs
Inputs
2 Pyruvate → 2 Acetyl CoA
2 ATP 8 NADH
2 Oxaloacetate
CITRIC ACID
CYCLE
6 CO2 2 FADH2
? What molecular products indicate the complete oxidation of glucose during cellular respiration?
CONCEPT 9.4
During oxidative phosphorylation, chemiosmosis couples electron transport to ATP synthesis (pp. 174-179)
■ NADH and FADH2 transfer electrons to the electron transport chain. Electrons move down the chain, losing energy in several energy-releasing steps. Finally, electrons are passed to O2, reducing it to H2O.
Protein complex of electron carriers
NADH
INTERMEMBRANE SPACE
Cyt c
IV
FADH, FAD
2 H* +/1⁄2 02
H2O
NAD+
MITOCHONDRIAL MATRIX
CONCEPT 9.5
Fermentation and anaerobic respiration enable cells to produce ATP without the use of oxygen (pp. 179–182)
■Glycolysis nets 2 ATP by substrate-level phosphorylation, whether oxygen is present or not. Under anaerobic conditions, anaerobic respiration or fermentation can take place. In anaerobic respira- tion, an electron transport chain is present with a final electron acceptor other than oxygen. In fermentation, the electrons from NADH are passed to pyruvate or a derivative of pyruvate, regen- erating the NAD* required to oxidize more glucose. Two common types of fermentation are alcohol fermentation and lactic acid fermentation.
■Fermentation and anaerobic or aerobic respiration all use glycolysis to oxidize glucose, but they differ in their final electron acceptor and whether an electron transport chain is used (respiration) or not (fermentation). Respiration yields more ATP; aerobic respira- tion, with O2 as the final electron acceptor, yields about 16 times as much ATP as does fermentation.
■ Glycolysis occurs in nearly all organisms and is thought to have evolved in ancient prokaryotes before there was O2 in the atmosphere.
? Which process yields more ATP, fermentation or anaerobic respiration? Explain.
CONCEPT 9.6
Glycolysis and the citric acid cycle connect
to many other metabolic pathways (pp. 182-184)
■ Catabolic pathways funnel electrons from many kinds of organic molecules into cellular respiration. Many carbohydrates can enter glycolysis, most often after conversion to glucose. Amino acids of proteins must be deaminated before being oxidized. The fatty acids of fats undergo beta oxidation to two-carbon frag- ments and then enter the citric acid cycle as acetyl CoA. Anabolic pathways can use small molecules from food directly or build other substances using intermediates of glycolysis or the citric acid cycle.
■ Cellular respiration is controlled by allosteric enzymes at key points in glycolysis and the citric acid cycle.
? Describe how the catabolic pathways of glycolysis and the citric acid cycle intersect with anabolic pathways in the metabolism of a cell.
(carrying electrons from food)

■ Along the electron transport chain, electron transfer causes protein complexes to move H* from the mitochondrial matrix (in eukaryotes) to the intermem- brane space, storing energy as a proton-motive force (H* gradi- ent). As Ht diffuses back into the matrix through ATP synthase, its passage drives the phosphory- lation of ADP to form ATP, called chemiosmosis.
About 34% of the energy stored in a glucose molecule is trans- ferred to ATP during cellular respiration, producing a maxi- mum of about 32 ATP.
INTER- MEMBRANE SPACE
MITO-
CHONDRIAL MATRIX
-ATP synthase
ADP+ P H+
ATP

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 10.1
Photosynthesis converts light energy to the chemical energy of food (pp. 189–192)
■ In eukaryotes that are autotrophs, photosynthe- sis occurs in chloroplasts, organelles containing thylakoids. Stacks of thylakoids form grana. Photosynthesis is summarized as
VOCAB SELF-QUIZ goo.gl/6u55ks
6 CO2+ 12 H2O + Light energy → C6H12O6 + 6 O2 + 6 H2O. Chloroplasts split water into hydrogen and oxygen, incorporating the electrons of hydrogen into sugar molecules. Photosynthesis is a redox process: H2O is oxidized, and CO2 is reduced. The light reactions in the thylakoid membranes split water, releasing O2, producing ATP, and forming NADPH. The Calvin cycle in the stroma forms sugar from CO2, using ATP for energy and NADPH for reducing power.
? Compare the roles of CO2 and H2O in cellular respiration and photosynthesis.
CONCEPT 10.2
The light reactions convert solar energy to the chemical energy of ATP and NADPH (pp. 192-201)
■Light is a form of electromagnetic energy. The colors we see as visible light include those wavelengths that drive photosynthe- sis. A pigment absorbs light of specific wavelengths; chlorophyll a is the main photosynthetic pigment in plants. Other accessory pig- ments absorb different wavelengths of light and pass the energy on to chlorophyll a.
■ A pigment goes from a ground state to an excited state when a photon of light boosts one of the pigment's electrons to a higher-energy orbital. This excited state is unstable. Electrons from isolated pigments tend to fall back to the ground state, giving off heat and/or light.
■ A photosystem is composed of a reaction-center complex surrounded by light-harvesting complexes that funnel the energy of photons to the reaction-center complex. When a special pair of reaction-center chlorophyll a molecules absorbs energy, one of its electrons is boosted to a higher energy level and transferred to the primary electron acceptor. Photosystem II contains P680 chlorophyll a molecules in the reaction-center complex; photosystem I contains P700 molecules.
■ Linear electron flow during the light reactions uses both photosystems and produces NADPH, ATP, and oxygen:
1,0
0,
Primary electron acceptor
Electron transport
chain
Cytochrome
complex
Pc
Electron transport chain
Primary electron acceptor
Fd
ATP?
Photosystem I
Photosystem II
NADP+ reductase
-NADP+ + H+ NADPH
■ Cyclic electron flow employs only one photosystem, produc- ing ATP but no NADPH or O2.
■During chemiosmosis in both mitochondria and chloroplasts, electron transport chains generate an H* gradient across a membrane. ATP synthase uses this proton-motive force to make ATP.
? The absorption spectrum of chlorophyll a differs from the action spectrum of photosynthesis. Explain this observation.
CONCEPT 10.3
The Calvin cycle uses the chemical energy of ATP and NADPH to reduce CO2 to sugar (pp. 201-202)
■The Calvin cycle occurs in the stroma, using electrons from NADPH and energy from ATP. One molecule of G3P exits the cycle per three CO2 molecules fixed and is converted to glucose and other organic molecules.
3 CO2
Carbon fixation
3 x 5C
6 x 3C
Calvin Cycle
Regeneration of CO2 acceptor
5 x 3C
1 G3P (3C)
Reduction
DRAW IT ➤ On the diagram above, draw where ATP and NADPH are used and where rubisco functions. Describe these steps.
CONCEPT 10.4
Alternative mechanisms of carbon fixation have evolved in hot, arid climates (pp. 203-206)
■ On dry, hot days, C3 plants close their stomata, conserving water but keeping CO2 out and O2 in. Under these conditions, photorespiration can occur: Rubisco binds O2 instead of CO2, consuming ATP and releasing CO2 without producing ATP or car- bohydrate. Photorespiration may be an evolutionary relic, and it may play a photoprotective role.
■ C4 plants minimize the cost of photorespiration by incorporat- ing CO2 into four-carbon compounds in mesophyll cells. These compounds are exported to bundle-sheath cells, where they release carbon dioxide for use in the Calvin cycle.
■ CAM plants open their stomata at night, incorporating CO2 into organic acids, which are stored in mesophyll cells. During the day, the stomata close, and the CO2 is released from the organic acids for use in the Calvin cycle.
■ Organic compounds produced by photosynthesis provide the energy and building material for Earth's ecosystems.
? Why are C, and CAM photosynthesis more energetically expensive than C, photosynthesis? What climate conditions would favor C and CAM plants?

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 11.1
External signals are converted to responses within the cell (pp. 213–217)
VOCAB SELF-QUIZ goo.gl/6u55ks
■ Signal transduction pathways are crucial for many processes. Signaling during yeast cell mating has much in common with processes in multicellu- lar organisms, suggesting an early evolutionary origin of signaling mechanisms. Bacterial cells can sense the local density of bacte- rial cells (quorum sensing).
■Local signaling by animal cells involves direct contact or the secre- tion of local regulators. For long-distance signaling, animal and plant cells use hormones; animals also pass signals electrically. Like epinephrine, other hormones that bind to membrane recep- tors trigger a three-stage cell-signaling pathway:
◊ Reception
Receptor
Signaling molecule
Transduction
Response
Activation of cellular response
Relay molecules
? What determines whether a cell responds to a hormone such as epinephrine? What determines how a cell responds to such a hormone?
CONCEPT 11.2
Reception: A signaling molecule binds
to a receptor protein, causing it to change shape (pp. 217-221)
The binding between signaling molecule (ligand) and receptor is highly specific. A specific shape change in a receptor is often the initial transduction of the signal.
■There are three major types of cell-surface transmembrane receptors: (1) G protein-coupled receptors (GPCRs) work with cytoplas- mic G proteins. Ligand binding activates the receptor, which then activates a specific G protein, which activates yet another pro- tein, thus propagating the signal. (2) Receptor tyrosine kinases (RTKs) react to the binding of signaling molecules by forming dimers and then adding phosphate groups to tyrosines on the cyto- plasmic part of the other monomer making up the dimer. Relay proteins in the cell can then be activated by binding to different phosphorylated tyrosines, allowing this receptor to trigger several pathways at once. (3) Ligand-gated ion channels open or close in response to binding by specific signaling molecules, regulating the flow of specific ions across the membrane.
The activity of all three types of receptors is crucial; abnormal GPCRs and RTKs are associated with many human diseases. ■ Intracellular receptors are cytoplasmic or nuclear proteins. Signaling molecules that are hydrophobic or small enough to cross the plasma membrane bind to these receptors inside the cell.
? How are the structures of a GPCR and an RTK similar? How does initiation of signal transduction differ for these two types of receptors?
CONCEPT 11.3
Transduction: Cascades of molecular interactions relay signals from receptors to target molecules in the cell (pp. 221-225)
At each step in a signal transduction pathway, the signal is trans- duced into a different form, which commonly involves a shape change in a protein. Many signal transduction pathways include phosphorylation cascades, in which a series of protein kinases each add a phosphate group to the next one in line, activating it. Enzymes called protein phosphatases remove the phosphate groups. The balance between phosphorylation and dephosphorylation regulates the activity of proteins involved in the sequential steps of a signal transduction pathway.
■ Second messengers, such as the small molecule cyclic AMP (CAMP) and the ion Ca2, diffuse readily through the cytosol and thus help broadcast signals quickly. Many G proteins activate adenylyl cyclase, which makes cAMP from ATP. Cells use Ca2+ as a second messenger in both GPCR and RTK pathways. The tyro- sine kinase pathways can also involve two other second messen- gers, diacylglycerol (DAG) and inositol trisphosphate (IP3). IP, can trigger a subsequent increase in Ca2+ levels.
? What is the difference between a protein kinase and a second
messenger? Can both operate in the same signal transduction pathway?
CONCEPT 11.4
Response: Cell signaling leads to regulation of transcription or cytoplasmic activities (pp. 226-229)
■Some pathways lead to a nuclear response: Specific genes are turned on or off by activated transcription factors. In others, the response involves cytoplasmic regulation.
■ Cellular responses are not simply on or off; they are regulated at many steps. Each protein in a signaling pathway amplifies the sig- nal by activating multiple copies of the next component; for long pathways, the total amplification may be over a millionfold. The combination of proteins in a cell confers specificity in the signals it detects and the responses it carries out. Scaffolding proteins increase signaling efficiency. Pathway branching further helps the cell coordinate signals and responses. Signal response can be terminated quickly because ligand binding is reversible. ? What mechanisms in the cell terminate its response to a signal and maintain its ability to respond to new signals?
CONCEPT 11.5
Apoptosis integrates multiple cell-signaling pathways (pp. 229-231)
Apoptosis is a type of programmed cell death in which cell components are disposed of in an orderly fashion. Studies of the soil worm Caenorhabditis elegans clarified molecular details of the relevant signaling pathways. A death signal leads to activation of caspases and nucleases, the main enzymes involved in apoptosis. ■ Several apoptotic signaling pathways exist in the cells of humans and other mammals, triggered in different ways. Signals eliciting apoptosis can originate from outside or inside the cell.
? What is an explanation for the similarities between genes in yeasts, nematodes, and mammals that control apoptosis?

''',

'''

SUMMARY OF KEY CONCEPTS
■ Unicellular organisms reproduce by cell division; multicellular organisms depend on cell division for their development from a fertilized egg and for growth and repair. Cell division is part of the cell cycle, an ordered sequence of events in the life of a cell.
CONCEPT 12.1
VOCAB
SELF-QUIZ goo.gl/6u55ks
Most cell division results in genetically identical daughter cells (pp. 235-237)
■ The genetic material (DNA) of a cell-its genome-is partitioned among chromosomes. Each eukaryotic chromosome consists of one DNA molecule associated with many proteins. Together, the complex of DNA and associated proteins is called chromatin. The chromatin of a chromosome exists in different states of condensation at different times. In animals, gametes have one set of chromosomes and somatic cells have two sets. ■ Cells replicate their genetic material before they divide, each daughter cell receiving a copy of the DNA. Prior to cell divi- sion, chromosomes are duplicated. Each one then consists of two identical sister chromatids joined along their lengths by sister chromatid cohesion and held most tightly together at a constricted region at the centromeres. When this cohesion is broken, the chromatids separate during cell division, becoming the chromosomes of the daughter cells. Eukaryotic cell division consists of mitosis (division of the nucleus) and cytokinesis (division of the cytoplasm).
? Differentiate between these terms: chromosome, chromatin, and chromatid.
CONCEPT 12.2
The mitotic phase alternates with interphase in the cell cycle (pp. 237-244)
■ Between divisions, a cell is in interphase: the G1, S, and G2 phases. The cell grows throughout interphase, with DNA being replicated only during the synthesis (S) phase. Mitosis and cytokinesis make up the mitotic (M) phase of the cell cycle.
Telophase and Cytokinesis
Cytokinesis Mitosis
MITOTIC (M) PHASE
INTERPHASE
Prometaphase
Anaphase
Metaphase
Prophase

The mitotic spindle, made up of microtubules, controls chro- mosome movement during mitosis. In animal cells, it arises from the centrosomes and includes spindle microtubules and asters. Some spindle microtubules attach to the kinetochores of chro- mosomes and move the chromosomes to the metaphase plate. After sister chromatids separate, motor proteins move them along kinetochore microtubules toward opposite ends of the cell. The cell elongates when motor proteins push nonkinetochore micro- tubules from opposite poles away from each other.
■ Mitosis is usually followed by cytokinesis. Animal cells carry out cytokinesis by cleavage, and plant cells form a cell plate.
During binary fission in bacteria, the chromosome replicates and the daughter chromosomes actively move apart. Some of the proteins involved in bacterial binary fission are related to eukary- otic actin and tubulin.
Since prokaryotes preceded eukaryotes by more than a billion years, it is likely that mitosis evolved from prokaryotic cell divi- sion. Certain unicellular eukaryotes exhibit mechanisms of cell division that may be similar to those of ancestors of existing eukaryotes. Such mechanisms might represent intermediate steps in the evolution of mitosis.
? In which of the three phases of interphase and the stages of mitosis do chromosomes exist as single DNA molecules?
CONCEPT 12.3
The eukaryotic cell cycle is regulated
by a molecular control system (pp. 244-250)
■ Signaling molecules present in the cytoplasm regulate progress through the cell cycle.
The cell cycle control system is molecularly based. Cyclic changes in regulatory proteins work as a cell cycle clock. The key molecules are cyclins and cyclin-dependent kinases (Cdks). The clock has specific checkpoints where the cell cycle stops until a go-ahead signal is received; important check- points occur in G1, G2, and M phases. Cell culture has enabled researchers to study the molecular details of cell division. Both internal signals and external signals control the cell cycle check- points via signal transduction pathways. Most cells exhibit density-dependent inhibition of cell division as well as anchorage dependence.
■ Cancer cells elude normal cell cycle regulation and divide unchecked, forming tumors. Malignant tumors invade nearby tissues and can undergo metastasis, exporting cancer cells to other sites, where they may form secondary tumors. Recent cell cycle and cell signaling research, and new techniques for sequencing DNA, have led to improved cancer treatments.

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 13.1
Offspring acquire genes from parents by inheriting chromosomes (pp. 255-256)
Each gene in an organism's DNA exists at a specific locus on a certain chromosome.
VOCAB SELF-QUIZ goo.gl/6u55ks
In asexual reproduction, a single parent produces genetically identical offspring by mitosis. Sexual reproduction combines genes from two parents, leading to genetically diverse offspring.
? Explain why human offspring resemble their parents but are not identical to them.
CONCEPT 13.2
Fertilization and meiosis alternate in sexual
life cycles (pp. 256-259)
■Normal human somatic cells are diploid. They have 46 chromo- somes made up of two sets of 23, one set from each parent. Human diploid cells have 22 pairs of homologs that are autosomes, and one pair of sex chromosomes; the latter typically determines whether the person is female (XX) or male (XY).
In humans, ovaries and testes produce haploid gametes by meiosis, each gamete containing a single set of 23 chromosomes (n = 23). During fertilization, an egg and sperm unite, forming a diploid (2n = 46) single-celled zygote, which develops into a multicellular organism by mitosis.
Sexual life cycles differ in the timing of meiosis relative to fertil- ization and in the point(s) of the cycle at which a multicellular organism is produced by mitosis.
? Compare the life cycles of animals and plants, mentioning their similarities and differences.
CONCEPT 13.3
Meiosis reduces the number of chromosome sets from diploid to haploid (pp. 259-265)
■The two cell divisions of meiosis, meiosis I and meiosis II, pro- duce four haploid daughter cells. The number of chromosome sets is reduced from two (diploid) to one (haploid) during meiosis I.
■ Meiosis is distinguished from mitosis by three events of meiosis I:
Prophase I: Each pair of homologous chromosomes undergoes synapsis and crossing over between nonsister chromatids with the subsequent appearance of chiasmata.
Metaphase I: Chromosomes line up as homologous pairs on the metaphase plate.
Anaphase I: Homologs separate from each other; sister chromatids remain joined at the centromere.
Meiosis II separates the sister chromatids.

■ Sister chromatid cohesion and crossing over allow chiasmata to hold homologs together until anaphase I. Cohesins are cleaved along the arms at anaphase I, allowing homologs to separate, and at the centromeres in anaphase II, releasing sister chromatids. ? In prophase I, homologous chromosomes pair up and undergo synapsis and crossing over. Can this also occur during prophase II? Explain.
CONCEPT 13.4
Genetic variation produced in sexual life cycles contributes to evolution (pp. 265-267)
■Three events in sexual reproduction contribute to genetic variation in a population: independent assortment of chromosomes during meiosis I, crossing over during meiosis I, and random fertilization of egg cells by sperm. During crossing over, DNA of nonsister chro- matids in a homologous pair is broken and rejoined.
■ Genetic variation is the raw material for evolution by natural selec- tion. Mutations are the original source of this variation; recombi- nation of variant genes generates additional genetic diversity.

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 14.1
Mendel used the scientific approach to identify two laws of inheritance (pp. 270-276)
Gregor Mendel formulated a theory of inheritance based on experiments with garden peas, proposing
VOCAB SELF-QUIZ goo.gl/6u55ks
that parents pass on to their offspring discrete genes that retain their identity through generations. This theory includes two "laws." The law of segregation states that genes have alternative forms, or alleles. In a diploid organism, the two alleles of a gene segregate (separate) during meiosis and gamete formation; each sperm or egg carries only one allele of each pair. This law explains the 3:1 ratio of F2 phenotypes observed when monohybrids self-pollinate. Each organism inherits one allele for each gene from each parent. In heterozygotes, the two alleles are different; expression of the dominant allele masks the phenotypic effect of the recessive allele. Homozygotes have identical alleles of a given gene and are therefore true-breeding.
The law of independent assortment states that the pair of alleles for a given gene segregates into gametes independently of the pair of alleles for any other gene. In a cross between dihybrids (individuals heterozygous for two genes), the offspring have four phenotypes in a 9:3:3:1 ratio.
CONCEPT 14.2
Probability laws govern Mendelian inheritance (pp. 276-278)
Rr Segregation of alleles into sperm
Sperm
1/2
R
ONE CEN
The multiplication rule states that the probability of two or more events occurring together is equal to the product of the individual probabilities of the independent single events. The addition rule states that the probability of an event that can occur in two or more independent, mutually exclusive ways is the sum of the individual probabilities.
■The rules of probability can be used to solve complex genetics problems. A dihybrid or other multicharacter cross is equiva- lent to two or more independent monohybrid crosses occur- ring simultaneously. In calculating the chances of the various offspring genotypes from such crosses, each character is first considered separately and then the individual probabilities are multiplied.
DRAWS

CONCEPT 14.3
Inheritance patterns are often more complex than predicted by simple Mendelian genetics (pp. 278-283)
■ Extensions of Mendelian genetics for a single gene:
Relationship among alleles of a single gene
Complete dominance of one allele
Description
Example
Heterozygous phenotype same as that of homo- zygous dominant
PP
Pp
Heterozygous phenotype
intermediate between
CONCEPT 14.4
Many human traits follow Mendelian patterns of inheritance (pp. 284-290)
■ Analysis of family pedigrees can be used to deduce the possible genotypes of individuals and make predictions about future off- spring. Such predictions are statistical probabilities rather than certainties.
Ww
ww
ww
Ww
Incomplete dominance
of either allele
Codominance
the two homozygous phenotypes
Both phenotypes expressed in heterozygotes
Ww ww ww Ww
Ww
ww
CRCR CRCW CWCW
IAB
WW ww
or
Multiple alleles
In the population, some genes have more than two alleles
ABO blood group alleles 1,1, i
Pleiotropy
One gene affects multiple phenotypic characters
Sickle-cell disease
Extensions of Mendelian genetics for two or more genes:
Relationship among
two or more genes
Epistasis
Description
The phenotypic
expression of one gene affects the expression of another gene
BE
bE
Example
BbEe
BbEe
(BE) (BE) (Be) (be)
AAAA BeAA
9
3
Polygenic inheritance
A single phenotypic character is affected by two or more genes
AaBbCc Xe AaBbCc
■The expression of a genotype can be affected by environmental influences, resulting in a range of phenotypes. Polygenic characters that are also influenced by the environment are called multifactorial characters.
■ An organism's overall phenotype, including its physical appear- ance, internal anatomy, physiology, and behavior, reflects its overall genotype and unique environmental history. Even in more complex inheritance patterns, Mendel's fundamental laws still apply.
Widow's peak
Ww
No widow's peak
Many genetic disorders are inherited as simple recessive traits. Most affected (homozygous recessive) individuals are children of phenotypically normal, heterozygous carriers. The sickle-cell allele has probably persisted for evolutionary reasons: Homozygotes have sickle-cell disease, but heterozygotes have an advantage because one copy of the sickle-cell allele reduces both the frequency and severity of malaria attacks. Sickle-cell alleles
Low
F-8-/-c-
Sickle-cell hemoglobin proteins
Part of a fiber of
sickle-cell hemo- globin proteins
Long fibers cause red blood cells to be sickle-shaped
Sickle- cell
disease
Lethal dominant alleles are eliminated from the population if affected people die before reproducing. Nonlethal dominant alleles and lethal ones that strike relatively late in life can be inherited in a Mendelian way.
■Many human diseases are multifactorial—that is, they have both genetic and environmental components and do not follow simple Mendelian inheritance patterns.
Using family histories, genetic counselors help couples deter- mine the probability that their children will have genetic dis- orders. Genetic testing of prospective parents to reveal whether they are carriers of recessive alleles associated with specific disorders has become widely available. Blood tests can screen for certain disorders in a fetus. Amniocentesis and chorionic villus sampling can indicate whether a suspected genetic dis- order is present in a fetus. Other genetic tests can be performed after birth.
? Both members of a couple know that they are carriers of the cystic fibrosis allele. None of their three children has cystic fibrosis, but any one of them might be a carrier. The couple would like to have a fourth

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 15.1
Morgan showed that Mendelian
inheritance has its physical basis in the behavior of chromosomes: scientific inquiry (pp. 296-297)
VOCAB SELF-QUIZ goo.gl/6u55ks
■ Morgan's work with an eye color gene in Drosophila led to the chromosome theory of inheritance, which states that genes are located on chromosomes and that the behavior of chromosomes during meiosis accounts for Mendel's laws. ? What characteristic of the sex chromosomes allowed Morgan to correlate their behavior with that of the alleles of the eye color gene?
CONCEPT 15.2
Sex-linked genes exhibit unique patterns of inheritance (pp. 298-300)
■ Sex is often chromosomally based. Humans and other mammals have an X-Y system in which sex is largely determined by whether a Y chromosome is present. Other systems are found in birds, fishes, and insects.
■The sex chromosomes carry sex-linked genes, virtually all of which are on the X chromosome (X-linked). Any male who inherits a recessive X-linked allele (from his mother) will express the trait, such as color blindness.
■ In mammalian females, one of the two X chromosomes in each cell is randomly inactivated during early embryonic develop- ment, becoming highly condensed into a Barr body.
? Why are males affected by X-linked disorders much more often
than females?
CONCEPT 15.3
Linked genes tend to be inherited together because they are located near each other on the same chromosome (pp. 301-306)
Sperm
P generation gametes
This F, cell has 2n = 6 chromo- somes and is heterozygous for all six genes shown (AaBbCcDdEeFf). Red = maternal; blue = paternal.
Each chromosome has hundreds or thousands of genes. Four (A, B, C, F) are shown on this one.
869
Egg
The alleles of unlinked genes are either on separate chromosomes (such as d and e)
or so far apart on the
same chromosome (e and f) that they assort independently.
Genes on the same chromo- some whose alleles are so close together that they do not assort independently (such as a, b, and c) are said to be genetically linked.
An F, dihybrid testcross yields parental types with the same combination of traits as those in the P generation parents and recombinant types (recombinants) with new combina- tions of traits not seen in either P generation parent. Because of the independent assortment of chromosomes, unlinked genes exhibit a 50% frequency of recombination in the gametes. For genetically linked genes, crossing over between nonsister chromatids during meiosis I accounts for the observed recombi- nants, always less than 50%.
The order of genes on a chromosome and the relative distances between them can be deduced from recombination frequencies observed in genetic crosses. These data allow construction of a linkage map (a type of genetic map). The farther apart genes are, the more likely their allele combinations will be recombined during crossing over.
? Why are specific alleles of two distant genes more likely to show recombination than those of two closer genes?
CONCEPT 15.4
Alterations of chromosome number or structure cause some genetic disorders (pp. 306-309)
■ Aneuploidy, an abnormal chromosome number, can result from nondisjunction during meiosis. When a normal gamete unites with one containing two copies or no copies of a particular chromosome, the resulting zygote and its descendant cells either have one extra copy of that chromosome (trisomy, 2n + 1) or are missing a copy (monosomy, 2n − 1). Polyploidy (extra sets of chromosomes) can result from complete nondisjunction. Chromosome breakage can result in alterations of chromo- some structure: deletions, duplications, inversions, and translocations. Translocations can be reciprocal or nonreciprocal.
■Changes in the number of chromosomes per cell or in the struc- ture of individual chromosomes can affect the phenotype and, in some cases, lead to disorders. Such alterations cause Down syndrome (usually due to trisomy of chromosome 21), certain cancers associated with chromosomal translocations that occur during mitosis, and various other human disorders.
? Why are inversions and reciprocal translocations less likely to be lethal than are aneuploidy, duplications, deletions, and nonreciprocal translocations?
CONCEPT 15.5
Some inheritance patterns are exceptions to standard Mendelian inheritance (pp. 310-311)
In mammals, the phenotypic effects of a small number of particu- lar genes depend on which allele is inherited from each parent, a phenomenon called genomic imprinting. Imprints are formed during gamete production, with the result that one allele (either maternal or paternal) is not expressed in offspring.
■ The inheritance of traits controlled by the genes present in mitochondria and plastids depends solely on the maternal par- ent because the zygote's cytoplasm containing these organelles comes from the egg. Some diseases affecting the nervous and muscular systems are caused by defects in mitochondrial genes that prevent cells from making enough ATP.
? Explain how genomic imprinting and inheritance of mitochondrial
and chloroplast DNA are exceptions to standard Mendelian inheritance.

'''

]

math_prompt = "This is a math question. Unlike other kinds of questions, you will not be asking for terms like 'what method allows you to do this' or 'what is the name of this formula.' Everything is centered around calculations and computations."

import time

def generate_science_bowl_question(temp_category, retrieved_text, difficulty, category, topic, question_style, question_example, question_instructions):
        prompt = ""
        energy_prompt = f"This is an energy question. In energy questions, you will briefly mention research being done at a random lab - e.g. Sandia National Labs, Ames Laboratory, Argonne National Laboratory, Brookhaven National Laboratory, Fermi National Accelerator Laboratory, Frederick National Laboratory for Cancer Research, Idaho National Laboratory, Lawrence Berkeley National Laboratory, Lawrence Livermore National Laboratory. After that, you will ask a random {temp_category} question based on that research. Do this for both the toss-up question and the bonus question."
        if(category=="Energy"):
            print("YES")
            prompt += energy_prompt
        elif(category=="Math"):
            prompt += math_prompt

        prompt += "The question should be difficult. The meaning of difficult is that it covers less-known, obscure terms."
        
        prompt +=  f"""

        Use this question {question_example} as a reference while creating the style of the toss-up and the bonus.

        To explain, the question presented is a {question_style} type of question: {question_instructions}.

        Both the toss-up and bonus must follow this format!! They both must be {question_style}.

        DON'T USE ANY OF THE CONTEXT OF THE QUESTION PROVIDED FOR THE INFORMATION USED FOR YOUR QUESTION. THE CONTEXT WILL FOLLOW!
       
        The questions should be appropriate for college students.

        The start of the question must be labeled with this category: {category}.
        
        This is the specific subtopic {topic}, which shouldn't be labeled.

        Using ONLY this context {retrieved_text}, generate a Science Bowl question.

        In short answer questions, the answer should not be more than one word!!!!

        Science Bowl is an advanced high-school, challenging buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z).

        These questions are read out loud. Make sure that the questions are 50-50 multiple-choice and short answer, and ensure that no short answer questions ask to explain anything - short answers answers should be either a term or a number resulting from a calculation (one word max). Also ensure that in multiple-choice questions, there are 4 choices and each choice is designated with the letters W, X, Y, and Z.

        DON'T ASK OPEN-ENDED QUESTIONS! SHORT ANSWER QUESTION ANSWERS ARE MEANT TO BE A SINGLE WORD, TERM, OR NUMBER. No asking for explanations or long equations!!!

        Also ensure that the answer to all questions is logical but still decently difficult and not just elementary school stuff. Even it's some randomly specific word, it should be clear from the context of the question. But make sure that these questions are challenging and made for advanced high-school level students.

        Using ONLY this context {retrieved_text}, generate a Science Bowl question.

        Once again, this is the category: {category}.

        NEVER EVER REFER TO THE PASSAGE. The competitors answering these questions do not have access to the context you are given.

        I want to EMPHASIZE SOME REALLY IMPORTANT INFORMATION now, PROBABLY THE MOST FREAKING IMPORTANTLY IMPORTANT INFORMATION HERE that you have to ENSURE that the question CAN BE ANSWERED solely using the provided context. If the context talks about something, you must incorporate the words of the context into your question. No adding of other information!! Otherwise I will make sure you don't generate a single response ever again.

        This means that someone should be able to answer your queston simply by looking at the context provided. No added information other than the context. I don't care what it is, no adding information outside of your narrow context. If that happens, I will kill myself.

        The question should be properly formatted and should not contain any errors.

        The questions should be appropriate for college students.

        """

        completion = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::AzCT79vQ",
            messages=[
                {"role": "developer", "content": "You ask Science Bowl questions. Science Bowl is a buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z.."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

def verify_science_bowl_question(temp_category, category, question, difficulty, question_style, question_example, question_instructions):
    prompt = "The question should be difficult. The meaning of difficult is that it covers less-known, obscure terms."
    energy_prompt = f"This is an energy question. In energy questions, you will briefly mention research being done at a random lab - e.g. Sandia National Labs, Ames Laboratory, Argonne National Laboratory, Brookhaven National Laboratory, Fermi National Accelerator Laboratory, Frederick National Laboratory for Cancer Research, Idaho National Laboratory, Lawrence Berkeley National Laboratory, Lawrence Livermore National Laboratory. After that, you will ask a random {temp_category} question based on that research. Do this for both the toss-up question and the bonus question. The category should be explicitly stated as Energy."
    if(category=="Energy"):
        prompt += energy_prompt

    prompt += f"""

    Keep in mind that this question {question_example} must be used as a reference for both the toss-up and the bonus!

    To explain, the question presented is a {question_style} type of question: {question_instructions}.

    Both the toss-up and bonus must follow this format!! They both must be {question_style}.

    The questions should be appropriate for advanced college students. What you're spewing out is middle school level questions. C'mon man!

    This is an AI-generated Science Bowl question: {question}.

    Your job is to make changes so that the question is appropriate for the Science Bowl competition.

    Ensure that ONLY this context {retrieved_text} is used!!

    Follow these criteria while verifying the validity and appropriateness of the question:
            - If it is short answer, does the answer require an explanation, an equation, or an open-ended, non-objective question? If so, change the question! No explanations or open-ended answers as answers! Everything in this competition is objective.
            - Does it require a calculator? If it does, make the numbers nicer or change the question entirely. The contestants solving these questions won't have access to a calculator.
            - Can the toss-up be solved in less than 5 seconds?
            - Can the bonus be solved in less than 20 seconds?
            - Does the question make the answer too obvious? (e.g. mentioning the answer in the question or hinting at it with a very obvious key word)
            - Does the question require any unnecessary assumptions? (e.g. having to guess the mass of an object if it's not given or guessing the molarity of a solution)
            - Participants will not have access to periodic tables or pages with constants, so does the question require knowledge of constants or specific values like atomic masses?
            - Is the question too easy? Make it more difficult!

    You should simply return a modified version of the question given. Make sure to make necessary changes.

    One super important thing you keep screwing up: especially for physics questions, in short answers, don't ask for explanations or equations. Only ask for numerical answers or one word terms!!!

    The questions should be appropriate for advanced college students. What you're spewing out is middle school level questions. C'mon man!

    """

    completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "developer", "content": "You modify Science Bowl questions. Science Bowl is a buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z.."},
                {"role": "user", "content": prompt}
            ]
        )
    return completion.choices[0].message.content

def similarity(question, user_answer):
    prompt = f"""

    This is the {question}.

    Assess the user's answer: {user_answer}.

    Give an explanation on how to solve the question.

    """
    completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "developer", "content": "You determine whether the user's answer is the same as the actual answer."},
                {"role": "user", "content": prompt}
            ]
    )
    return completion.choices[0].message.content

if "toss_up_answer" not in st.session_state:
    st.session_state.toss_up_answer = None
if "bonus_answer" not in st.session_state:
    st.session_state.bonus_answer = None
if "question_final" not in st.session_state:
    st.session_state.question_final = None
if "toss_up_attempt" not in st.session_state:
    st.session_state.toss_up_attempt = ""
if "bonus_attempt" not in st.session_state:
    st.session_state.bonus_attempt = ""
if "bonus_revealed" not in st.session_state:
    st.session_state.bonus_revealed = False

if st.button("Generate Question"):
    st.session_state.toss_up_attempt = ""
    st.session_state.bonus_attempt = ""
    st.session_state.bonus_revealed = False 

    category, topic = select_topic()
    index = 0
    if category != "Energy":
        for i in range(len(subtopics[category])):
            if subtopics[category][i] == topic:
                index = i
                break

    ans = []
    x = random.randint(0,2)
    if category == "Chemistry":
        ans = chem_text
    elif category == "Biology":
        ans = bio_text
    elif category == "Physics":
        ans = phys_text
    elif category == "Math":
        ans.append(subtopics[category][index])
        index = 0
    elif category == "Energy":
        if x == 0:
            ans = phys_text
        elif x == 1:
            ans = chem_text
        else:
            ans = bio_text

    temp_category = category

    if category=="Energy":
        index = 0
        if x == 0:
            temp_category = "Physics"
        elif x == 1:
            temp_category = "Chemistry"
        else:
            temp_category = "Biology"
        index = random.randint(0,len(subtopics[temp_category])-1)

    question_style = ""
    question_example = ""
    question_instructions = ""
    if temp_category=="Chemistry" or temp_category=="Biology" or temp_category=="Physics":
        x = random.randint(0,len(question_styles[temp_category])-1)
        question_style = question_styles[temp_category][x]
        question_example = question_styles_examples[temp_category][x]
        question_instructions = question_style_explanations[question_style]

    difficulty = 3
    print(category)
    retrieved_text = ans[index]
    print(retrieved_text)
    if category!="Math":
        location = random.randint(0, len(retrieved_text)-400)
        retrieved_text = retrieved_text[location:location+400]
    raw = generate_science_bowl_question(temp_category, retrieved_text, difficulty, category, topic, question_style, question_example, question_instructions)
    st.session_state.question_final = verify_science_bowl_question(temp_category, category, raw, difficulty, question_style, question_example, question_instructions)

if st.session_state.question_final:
    bonus_index = 0
    for i in range(len(st.session_state.question_final)):
        if st.session_state.question_final[i:i+5] == "BONUS" or st.session_state.question_final[i:i+5]=="Bonus":
            bonus_index = i

    tossup_ans_index = 0
    for i in range(len(st.session_state.question_final)):
        if st.session_state.question_final[i:i+6] == "ANSWER":
            tossup_ans_index = i
            break
    
    if(tossup_ans_index==0):
        tossup_ans_index = bonus_index

    bonus_ans_index = 0
    for i in range(len(st.session_state.question_final)):
        if st.session_state.question_final[i:i+6] == "ANSWER":
            bonus_ans_index = i
    
    if(bonus_ans_index==0):
        bonus_ans_index = len(st.session_state.question_final)-1
    
    toss_up = st.session_state.question_final[0:tossup_ans_index]
    bonus = st.session_state.question_final[bonus_index:bonus_ans_index]
    
    st.write("### Toss-Up Question:")
    st.write(toss_up)

    st.session_state.toss_up_attempt = st.text_input("Your Answer for Toss-Up:", st.session_state.toss_up_attempt)
    if st.session_state.toss_up_attempt:
        st.session_state.toss_up_answer = similarity(toss_up, st.session_state.toss_up_attempt)
        st.write(st.session_state.toss_up_answer)

    if st.button("Reveal Bonus"):
        st.session_state.bonus_revealed = True 

    if st.session_state.bonus_revealed:
        st.write("### Bonus Question:")
        st.write(bonus)

        st.session_state.bonus_attempt = st.text_input("Your Answer for Bonus:", st.session_state.bonus_attempt)
        if st.session_state.bonus_attempt:
            st.session_state.bonus_answer = similarity(bonus, st.session_state.bonus_attempt)
            st.write(st.session_state.bonus_answer)
