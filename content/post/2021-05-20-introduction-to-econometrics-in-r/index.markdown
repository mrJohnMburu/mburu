---
title: Introduction to Econometrics in R
author: 'John Mburu'
date: '2021-05-20'
slug: introduction-to-econometrics-in-r
categories: []
tags: [econometrics, economics, statistics, ols]
subtitle: ''
summary: ''
authors: []
lastmod: '2021-05-20T09:43:20+03:00'
featured: no
image:
  caption: ''
  focal_point: ''
  preview_only: no
projects: []
bibliography: citation.bib
---

## Introduction

Econometrics is a social science that applies the tools of economic theory, mathematics, and statistical inference to analyze economic data and explore causal relationships (Greene 2014). Hence, econometrics uses economic theory to make credible claim about human behavior, formulate the claim into mathematical equations and use statistical inference to measure whether the claim is statistically significance. For example, an economist may be interested to know whether the social programs like cash transfer program instituted by Kenya government during the Covid-19 pandemic cushioned family from the negative effect of the pandemic. The economist may claim that the cash transfer led to increase in household consumption. This is Keynesian theory of consumption. The economic theory helps the economist to formulate a hypothesis i.e. increase in income leads to increase in consumption. The hypothesis can either be true or false, and hence, the economist needs to test whether there is any relationship between income and consumption. There is a need to express the relationship in a mathematical form. Let assumes that income and consumption has a linear relationship i.e.

(1).\$ y\_i = \\alpha + \\beta x\_i \$

In equation (1) \$ y\_i \$ is consumption of individual \$ i \$ and \$ x\_i \$ is the income and \$ \\alpha \$ and \$ \\beta \$ are parameters. Our interest is to know whether \$ \\beta \$ is positive or not. Another restriction from Keynesian theory of consumption is that \$ 0 &lt; \\beta &lt; 1 \$.

Equation (1) above assumes that only income affect consumption and there is one-to-one relationship between income and consumption. However, in most economic applications the researcher is not able to observe all variables that can affect a \$ y\_i \$. Moreover, it is likely that the relationship between consumption and income is not perfect. Hence, we add an error term, that capture any other variable not included in the model, any specification errors and measurement errors.

(2).\$ y\_i = \\alpha + \\beta x\_i + e\_i \$

Different approach can be used to estimate the value \$ \\beta \$. This includes:

1.  Ordinary Least Square  
2.  Maximum Likelihood Estimation  
3.  Method of Moments

## Review of Ordinary Least square (OLS)

Since \$ e\_i \$ is unobservable, we need to make several assumptions to be estimate the value of \$ \\beta \$.

### Asumption of OLS

1.  Linearity- \$ y\_i = \\alpha + \\beta x\_i + e\_i \$  
2.  \$ E(e\_i) = 0 \$  
3.  \$ var(e\_i) = \\sigma^2 \$  
4.  \$ E(e\_i,e\_j) = 0 \$  
5.  \$ E(x\_i,e\_i) = 0 \$  
6.  No multicollinearity  
7.  \$ x\_i \$ is fixed in repeated samples  
8.  \$ e\_i \\sim N(0, \\sigma^2) \$  
9.  No outliers

### Estimation

The least square principle asserts that we can fit a line of best fit through the data by minimizing the sum of squared errors. Let us stack the \$ y\_i \$ observations into a matrix \$ Y \$, \$ x\_i \$ observations into matrix of \$ X \$, and \$ e\_i \$ values into matrix of \$ e \$. Hence, equation (2) can be written in matrix form as:

(3).\$ Y = X \\beta + e \$  

where \$ Y \$ is \$ N x 1 \$ vector of dependent variable,
\$ X \$ is \$ N x K \$ matrix of independent variables,
\$ e \$ is \$ N x 1 \$ vector of errors, and
\$ \\beta \$ is a \$ Kx1 \$ vector of parameters to be estimated.

Equation (3) can be expressed as;

(4).\$ e = Y-X \\beta \$

The aim is to minimize the sum of squared residuals.

(5).\$e’e = (Y-X \\beta)’(Y-X \\beta) \$

Minimizing the sum of squared residuals, we get:

(6).\$ \\hat \\beta = (X’X)^{-1}X’Y \$

### Illustration

Let us use simulation to illustration linear regression in R.I simulate data x and Y, and assume the value of \$ \\beta \$ is 2 and the value of \$ \\alpha \$ is 40. The number of observation is 100. I assume x is normally distributed with a mean of 30 and a standard deviation of 10 while error terms are normally distributed with a mean of zero and a standard deviation of 4.

``` r
set.seed(1)
#Simulate 100 observations with mean of 30 and standard deviation of 10.
x <- rnorm(100, 30, 10)
#Simulate 100 observations with a mean of 0 and standard deviation of 4.
e <- rnorm(100, 0, 4)
# Generate y as a linear function of x and e.
y <- 40 + 2*x + e
# use lm() function, to run a linear regression
print(lm(y ~ x))
```

    ## 
    ## Call:
    ## lm(formula = y ~ x)
    ## 
    ## Coefficients:
    ## (Intercept)            x  
    ##       39.86         2.00

As the output shows, the value of coefficient of \$ x \$ is 2 while the intercept is approximately 40.

What if were to use equation (6), what will we get? I start with an illustration to show how data used for regression is usually arranged. You have N individual, in our case N = 100. Each individual has a linear equation linking y and x. Hence, the vector of Y is a column vector of dependent variable and X is N by K matrix of independent variable. Where K is the number of independent variables. The first column of X is filled with 1’s as it corresponds to the intercept. The table below illustrates the data structure. You read x1,1 as “first independent variable for the first individual” and so on. x1 is the variable for the intercept, and it is equal to 1 while y and x2 has been generated above.

| Y    | X1     | X2     |
|------|--------|--------|
| y1   | x1,1   | x2,1   |
| y2   | x1,2   | x2,2   |
| .    | .      | .      |
| .    | .      | .      |
| .    | .      | .      |
| y100 | X1,100 | x2,100 |

Let us start by generating x1 is a vector of 1’s with a length of 100, and use equation (6) to calculate the value \$ \\beta \$.

``` r
#create a sequence of 1.
A <- seq(from =1, to = 1, length.out = 100)
#convert the x and y into matrices.
#The x and y generated above, contains the 100 values of each variables. I use transpose() function that returns a matrix, to transform x and y into matrices.
x_vec = t(x)
#bind the X_vec to the vector of 1's to create a matrix of 2 by 50.
X_row <- rbind(A, x_vec)
#Create a 50 by 2 matrix of X's i.e. x1 and x2.
X <- t(X_row)
#Create X transpose
X_trans <- t(X)

#create the matrix of X transpose X.
XtX <- X_trans%*%X

#Create y column vector
y_row <- t(y)
y_col <- t(y_row)

#Create the matrix of X transpose Y.
XTY <- X_trans%*%y_col

#Solve for inverse of XtX 
XtX_inv <- solve(XtX)

#Use equation (6) to calculate the value of coefficients.
print(XtX_inv%*%XTY)
```

    ##        [,1]
    ## A 39.861954
    ##    1.999576

The results shows that the value of intercept is approximately 40 while the coefficient \$ \\beta \$ is approximately 2. Hence, the R function lm() and the equation (6) give similar answers.

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-greene2014" class="csl-entry">

Greene, William. 2014. *Econometric Analysis*. Pearson Education.

</div>

</div>
