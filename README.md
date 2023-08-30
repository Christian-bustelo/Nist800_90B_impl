# Nist800_90B_impl

This repo contains a main execution file called "entropyMCV.py" that has the code for the validation and entropy calculation of a sequence of numbers. 
This schema follows the Nist 800_90B work, executing IID assumption tests, restart tests and entropy calculation with the "Most Common Value" estimator.
We include a file "testPermutacion.py" that contains the implementation of the functions that we will use in the main script in order to see if we must discard IID assumption.

For the use of the script you must change the two mocked points (only the first if you don't wanna use the restart test): The main load of data, and the matrix construction for the Restart Test (both marked whit the 'Mocked' Tag).

To the use you can run the code whit two options:

"-v" : This will allow you to see inter media data in the executions of the test as the initial entropy estimations or the Sanity Check results in the Restart Test.

"--no-test" : This option is used when you wanna skip Restart Test, in this case we only apply the validation of the IID hypothesis and then the calculus of the entropy.

We will be following the next schema but assuming that the data can´t be No IID because we are testing full random number generation.

![EstructuraTest](https://github.com/Christian-bustelo/Nist800_90B_impl/assets/137056718/7a09a14e-da0f-4a6d-ab53-1ebc040c57ae)
