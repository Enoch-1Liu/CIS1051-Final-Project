# Proposal

## What will (likely) be the title of your project?

Fourier Transform Visualization Using the ManimGL Library

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

The Fourier Transform is a mathematical tool that takes a function in the time domain and outputs another function in the frequency domain. This project details the action of the Fourier Transform, which is a highly visualizable process.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

The goal of this project is to use the ManimGL library (made by Grant Sanderson, better known as the creator of the Youtube account 3Blue1Brown) to visually demonstrate how the Fourier Transform decomposes a complex signal into individual frequency components. The animation begins with a signal formed by a combination of different sine waves, then goes through how the Fourier transform analyzes the signal and transitions it from the time domain (amplitute vs. time) to the frequency domain (magnitude vs. frequency). The final product will show how a complicated original waveform can be understood through simpler components.

The animation will be implemented mainly with the ManimGL library, with Seaborn and/or Matplotlib supporting if needed. NumPy will handle the calculations. There are a few main scenes:
1. Displaying individual sine waves
2. Combining sine waves into a complicated waveform
3. Animation of the Fourier transform
4. Displaying resulting frequency

## If planning to combine 1051's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to 1051, and which aspect(s) would relate to the other course?

The Fourier transform is applicable in Probability theory, so there is a possible overlap where the visualization can relate to probability theory, where the underlying coding is still related to CIS1051

## If planning to collaborate with 1 or 2 classmates for the final project, list their names, email addresses, and the names of their assigned TAs below.

Enoch Liu, enoch.liu@temple.edu, TA: Faegheh Seifhashemi

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

Implementing a Fourier transform visualization

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

Implementing a Fourier transform visualization along with a few miscellaneous visualizations. We are hoping to possibly visualize some 2D and 3D graphs, and if time permitting, matrices (e.g., matrix multiplication, vectorization)

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

Adding an interactable interface that allows users to request certain visualizations, like allowing users to input linear combinations.

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

Need to learn the ManimGL library in depth, and learn how to implement it correctly and represent the visualization correctly. We also need to understand the Fourier transform in depth, as it is a fairly complex mathematical concept. 
Things to do:
1. Learn to implement the ManimGL library
2. Understand the Fourier Transform
3. Understand the implications using NumPy, and additional resources using Seaborn and Matplotlib, if applicable
4. Implement additional visualization in 2D, 3D, and Matrix related equations
5. Implement an interface where users can interact
