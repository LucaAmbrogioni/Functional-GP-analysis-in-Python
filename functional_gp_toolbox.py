
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import random as rnd
import copy
import sys
sys.setrecursionlimit(1000)
get_ipython().magic(u'matplotlib inline')



class linear_tools(object):
    #
    def __init__(self):
        self.description = "This class contains linear algebra methods"
    #
    def matrix_division(self, divider, divided, side, cholesky):
        X = np.matrix(divided)
        if cholesky is "yes":
            M = np.matrix(np.linalg.cholesky(divider))
            if side is "right":
                first_division = np.linalg.solve(M,X.T).T
                result = np.linalg.solve(M.T,first_division.T).T
            elif side is "left":
                first_division = np.linalg.solve(M,X)
                result = np.linalg.solve(M.T,first_division)
            else:
                print "The side should be either left or right"
                return
        else:
            M = np.matrix(divider)
            if side is "right":
                result = np.linalg.solve(M.T,X.T).T
            elif side is "left":
                result = np.linalg.solve(M,X)
            else:
                print "The side should be either left or right"
                return
        return result


# 

class functional_tools(object):
    #
    def __init__(self):
        self.description = "This class contains several high order functions for manipulating lambdas"
    #
    def partial_application(self, bivariate_function, y_value):
        partial_function = lambda x: bivariate_function(x,y_value)
        return partial_function
    #
    def composition(self, first_function, second_function):
        composed_function = lambda x: second_function(first_function(x))
        return composed_function
    #
    def power(self, function, exponent):
        power_function = self.composition(function, lambda x: x**exponent)
        return power_function
    #
    def sum(self, first_function, second_function):
        summed_function = lambda x: first_function(x) + second_function(x)
        return summed_function
    #
    def product(self, first_function, second_function):
        product_function = lambda x: first_function(x)*second_function(x)
        return product_function
    #
    def difference(self, first_function, second_function):
        differenced_function = lambda x: first_function(x) - second_function(x)
        return differenced_function
    #
    def bivariate_sum(self, first_function, second_function):
        summed_function = lambda x,y: first_function(x,y) + second_function(x,y)
        return summed_function  
    #
    def bivariate_difference(self, first_function, second_function):
        differenced_function = lambda x,y: first_function(x,y) - second_function(x,y)
        return differenced_function 
    #
    def bivariate_product(self, first_function, second_function):
        product_function = lambda x,y: first_function(x,y)*second_function(x,y)
        return product_function
    #
    def bivariate_composition(self, bivariate_function, univariate_function):
        composed_function = lambda x,y: univariate_function(bivariate_function(x,y))
        return composed_function
    #
    def outer_product(self, first_function, second_function):
        multiplied_function = lambda x,y: first_function(x)*second_function(y)
        return multiplied_function
    #
    def scale(self, function, scale):
        scaled_function = lambda x: scale*function(x)
        return scaled_function
    #
    def bivariate_scale(self, function, scale):
        scaled_function = lambda x,y: scale*function(x,y)
        return scaled_function
    #
    def translate(function, c):
        translated_function = lambda x: function(x - c)
        return translated_function
    # 
    def gaussian_family(self, mu_function, var_function):
        gaussian_form = lambda x, mu, nu: (1/(np.sqrt(2*np.pi)*nu))*np.exp(-(x - mu)**2/(2.*nu))
        gaussian_family = lambda x,y: gaussian_form(x, mu_function(y), var_function(y))
        return gaussian_family
    #
    def linear_combination(self, functions_list, weights_list):
        if len(functions_list) == 1:
            combined_function = self.scale(functions_list[0], weights_list[0])
        else:
            scaled_function = self.scale(functions_list[-1], weights_list[-1])
            combined_function = self.sum(self.linear_combination(functions_list[:-1], 
                                                                 weights_list[:-1]), 
                                         scaled_function)
        return combined_function 
    # 
    def bivariate_linear_combination(self, functions_list, weights_list):
        if len(functions_list) == 1:
            combined_function = self.bivariate_scale(functions_list[0], weights_list[0])
        else:
            scaled_function = self.bivariate_scale(functions_list[-1], weights_list[-1])
            combined_function = self.bivariate_sum(self.bivariate_linear_combination(functions_list[:-1], 
                                                                                     weights_list[:-1]), 
                                                   scaled_function)
        return combined_function 
    #
    def translated_linear_combination(self, bivariate_function, weights_list, center_points):
        translated_functions_list = [self.partial_application(bivariate_function, point) for point in center_points]
        translated_combined_function = self.linear_combination(translated_functions_list, 
                                                               weights_list)
        return translated_combined_function
    #
    def translated_quadratic_combination(self, 
                                         bivariate_function, 
                                         weights_array, 
                                         first_center_points,
                                         second_center_points):
        if len(weights_array) == 1:
            combined_quadratic_function = self.outer_product(self.translated_linear_combination(bivariate_function, 
                                                                                                weights_array[0], 
                                                                                                first_center_points),
                                                             self.partial_application(bivariate_function, 
                                                                                      second_center_points[0]))
        else:
            combined_row = self.outer_product(self.translated_linear_combination(bivariate_function, 
                                                                                 weights_array[-1], 
                                                                                 first_center_points),
                                              self.partial_application(bivariate_function, 
                                                                       second_center_points[-1]))
            combined_quadratic_function = self.bivariate_sum(self.translated_quadratic_combination(bivariate_function, 
                                                                                                   weights_array[:-1], 
                                                                                                   first_center_points,
                                                                                                   second_center_points[:-1]), 
                                                             combined_row)
        return combined_quadratic_function
    #
    def diagonal(self, bivariate_function):
        diagonal_function = lambda x: bivariate_function(x,x)
        return diagonal_function
    #
    def real(self, function):
        return lambda x: np.real(function(x))

class covariance_functions(object):
    #
    fun_tools = functional_tools()
    
    class generic_covariance(object):
        #
        def __init__(self):
            self.function = lambda x,y: 0
            self.fourier = lambda xi: self.__raise_fourier_error()
        #
        def __add__(self, second_covariance):
            sum_covariance = self
            sum_covariance.function = covariance_functions.fun_tools.bivariate_sum(self.function, 
                                                                                   second_covariance.function)
            sum_covariance.fourier = covariance_functions.fun_tools.sum(self.fourier, 
                                                                        second_covariance.fourier)
            return sum_covariance
        #
        def __mul__(self, covariance_or_scalar):
            product_covariance = copy.copy(self)
            if (type(covariance_or_scalar) != float)&(type(covariance_or_scalar) != int):
                product_covariance.function = covariance_functions.fun_tools.bivariate_product(self.function, 
                                                                                               covariance_or_scalar.function)
                product_covariance.fourier = lambda xi: self.__raise_fourier_error()
            else:
                product_covariance.function = covariance_functions.fun_tools.bivariate_scale(self.function, 
                                                                                             float(covariance_or_scalar))
            return product_covariance
        #
        def __rmul__(self, covariance_or_scalar):
            return self.__mul__(covariance_or_scalar)
        #
        def transformation(self, mapping):
            transformed_covariance = copy.copy(self)
            transformed_covariance.function = lambda x,y: self.function(mapping(x),mapping(y))
            transformed_covariance.fourier = lambda xi: self.__raise_fourier_error()
            return transformed_covariance
        #
        def __raise_fourier_error(self):
            raise(NotImplementedError)
        #
        def __call__(self, x, y):
            return self.function(x, y)
    
    class squared_exponential(generic_covariance):
        #
        def __init__(self, length_scale):
            super(covariance_functions.squared_exponential, self).__init__()
            self.function = lambda x,y,s=length_scale: np.exp(-(x - y)**2/(2*s**2))
            self.fourier = lambda xi,s=length_scale: s*np.exp(-s**2*xi**2/(2))

    class quasi_harmonic(generic_covariance):
        #
        def __init__(self, frequency, length_scale):
            super(covariance_functions.quasi_harmonic, self).__init__()
            self.function = lambda x,y,f=2*np.pi*frequency,s=length_scale: np.exp(-(x - y)**2/(2*s**2))*np.cos(f*(x - y))
            self.fourier = lambda xi,f=2*np.pi*frequency,s=length_scale: 0.5*(s*np.exp(-s**2*(2*np.pi*xi-f)**2/(2)) 
                                                                              + s*np.exp(-s**2*(2*np.pi*xi+f)**2/(2)))

    class harmonic(generic_covariance):
        #
        def __init__(self, frequency):
            super(covariance_functions.harmonic, self).__init__()
            self.function = lambda x,y,f=2*np.pi*frequency: np.cos(f*(x - y))

    class polynomial(generic_covariance):
        #
        def __init__(self, order):
            super(covariance_functions.polynomial, self).__init__()
            self.function = lambda x,y,p = order: (x*y + 1)**p

    class periodic(generic_covariance):
        #
        def __init__(self, frequency, harmonicity):
            super(covariance_functions.periodic, self).__init__()
            self.function = lambda x,y,f = frequency, rho = harmonicity: np.exp(-2*np.sin(np.pi*f*(x - y))**2/rho**2) 

class kernel_tools(object):
    #
    def __init__(self):
        self.description = "This class contains methods for working with GP covariance functions (kernels)"
        self.covariance_functions = covariance_functions()
    #
    def get_polynomial_kernel(self, order):
        return self.covariance_functions.polynomial(order)
    #
    def get_squared_exponential_kernel(self, length_scale):
        return self.covariance_functions.squared_exponential(length_scale)
    #
    def get_harmonic_kernel(self, frequency):
        return self.covariance_functions.harmonic(frequency)
    #
    def get_quasi_harmonic_kernel(self, frequency, length_scale):
        return self.covariance_functions.quasi_harmonic(frequency, length_scale)
    #
    def get_periodic_kernel(self, frequency, harmonicity = 1.):
         return self.covariance_functions.periodic(frequency, harmonicity)
    #
    def get_kernel_array(self, kernel, x_range, y_range):
        meshgrid_1, meshgrid_2 = np.meshgrid(x_range, y_range)
        kernel_array = kernel(meshgrid_1, meshgrid_2)
        return kernel_array
    #
    def plot_kernel(self, kernel, x_range = np.arange(-2,2,0.01), y_range = np.arange(-2,2,0.01)):
        kernel_array = self.get_kernel_array(kernel, x_range, y_range)
        plt.imshow(kernel_array)
        plt.colorbar()
        return
    #
    def get_function_from_kernel(self, 
                                 kernel,
                                 number_functions = 1, 
                                 function_range = np.arange(-1,1,0.05),
                                 jitter = 10**-8):
        ## private functions ##
        def sample_functions(kernel_square_root, function_length, number):
            gaussian_white_noise = np.matrix(np.random.normal(loc = 0, 
                                                              scale = 1, 
                                                              size = (function_length,1)))
            generated_function = np.array(kernel_square_root*gaussian_white_noise).flatten()
            if number == 1:
                functions = [generated_function]
            else:
                functions = sample_functions(kernel_square_root, 
                                             function_length, 
                                             number = number - 1) + [generated_function]   
            return functions 
        ## main code ##
        function_length = len(function_range)
        kernel_array = self.get_kernel_array(kernel, function_range, function_range)
        jittered_kernel_matrix = np.matrix(kernel_array + jitter*np.identity(function_length))
        kernel_square_root = np.linalg.cholesky(jittered_kernel_matrix)
        sampled_functions = sample_functions(kernel_square_root, 
                                             function_length, 
                                             number = number_functions)
        return sampled_functions
    #
    def get_corrupted_samples(self, 
                              functions_list, 
                              sample_indices,
                              noise_level):
        ## private functions ##
        def get_datapoint(function, 
                          index,
                          noise_level = noise_level):
            datapoint = function[index] + np.random.normal(scale = noise_level)
            return datapoint  
        #
        def get_samples(function, 
                        indices = sample_indices,
                        noise_level = noise_level):
            return np.array([get_datapoint(function,index) for index in indices])
        ## main code ##
        sample_length = len(sample_indices)
        if len(functions_list) == 1:
            corrupted_samples = [get_samples(functions_list[0])]
        else:
            corrupted_samples = get_corrupted_samples(self, 
                                                      functions_list[:-1], 
                                                      sample_indices,
                                                      noise_level) + [get_samples(functions_list[-1])]
        return corrupted_samples    
    #
    def plot_samples(self, samples, indices, x_range):
        for index in indices:
            plt.plot(x_range, samples[index])
        return
    #
    def plot_corrupted_samples(self,
                               function_range, 
                               functions, 
                               sample_range, 
                               corrupted_samples,
                               plot_samples = "yes",
                               index = 0):
        plt.plot(function_range, functions[index], c = "k", label = "Sampled function")
        if plot_samples is "yes":
            plt.scatter(sample_range, corrupted_samples[index], label = "Data points")
        plt.title("Generated sample")
        plt.legend(loc="best")
        plt.xlim(min(function_range),max(function_range))
        return
#
class spectral_tools(object):
    #
    def __init__(self):
        self.description = "This class contains method for working with Fourier transforms"
        self.fun_tools = functional_tools()
        self.k_tools   = kernel_tools()
        self.covariance_functions = covariance_functions()
        self.fourier_component = lambda f,t0: np.exp(1j*2*np.pi*f*t0)
    #
    def get_fourier_kernels_list(self,
                                 kernel,
                                 center_points):
        if len(center_points) == 0:
            transformed_signal = []
        else:
            transformed_signal = (self.get_fourier_kernels_list(kernel,
                                                                center_points[:-1]) +
                                  [self.fun_tools.product(kernel.fourier, 
                                                          self.fun_tools.partial_application(self.fourier_component, 
                                                                                             center_points[-1]))])
        return transformed_signal
    #
    def get_fourier_transform(self,
                              kernel,
                              weights_list,
                              center_points):
        fourier_kernels_list = self.get_fourier_kernels_list(kernel,
                                                             center_points)
        fourier_transform = self.fun_tools.linear_combination(fourier_kernels_list, 
                                                              weights_list)
        return fourier_transform  
    #
    def get_DFT_spectrum(self, data_points):
        ts_length = len(data_points)
        tapered_time_series = np.multiply(np.hanning(ts_length),data_points)
        fourier = np.fft.fft(tapered_time_series, norm = "ortho")
        DFT_spectrum = np.fft.fftshift(np.abs(fourier))**2
        return DFT_spectrum
    #
    def get_frequency_range(self, time):
        time_step = np.median(np.diff(time))
        freq_range = np.fft.fftshift(np.fft.fftfreq(len(time))/time_step)
        return freq_range
    #
    
    #
    def get_BFG_covariance_function(self,
                                    time, 
                                    data_points, 
                                    noise_sd,
                                    spectral_width = 2*np.pi*0.025):
        ## private functions ##
        def get_spectral_weights(data_points,
                                 number_iterations = 15000,
                                 learning_rate = 2.5*10**-2):
            ## private functions ##
            def spectral_gradient_ascent(initial_spectral_weights,
                                         number_iterations, 
                                         learning_rate):
                ## private functions ##
                def update_iterator(current_log_weights, n):
                    if n == 0:
                        return current_log_weights
                    else:
                        log_gradient = get_spectrum_functional_gradient(current_log_weights)
                        new_log_weights = current_log_weights + learning_rate*log_gradient
                        return update_iterator(new_log_weights, n - 1)
                def get_spectrum_functional_gradient(current_log_weights):
                    prediction = spectrum_covariance_matrix*np.exp(current_log_weights) 
                    noise_contribution = np.ones(prediction.shape)*noise_sd**2
                    deviation_function = lambda predicted,observed: np.divide(observed - predicted, 
                                                                              np.power(predicted,2))
                    gradient = (0.5*spectrum_covariance_matrix*deviation_function(prediction + noise_contribution, 
                                                                                  data) # likelihood
                                - prediction) # prior 
                    log_gradient = np.multiply(np.exp(current_log_weights), gradient)
                    return log_gradient  
                ## main code ##
                data = np.matrix(np.reshape(DFT_spectrum, newshape = (DFT_spectrum.shape[1],1)))
                initial_log_weights = np.log(initial_spectral_weights)
                log_weights = update_iterator(initial_log_weights, n = number_iterations)
                spectral_weights = np.exp(log_weights)
                return list(np.array(spectral_weights).flatten())
            ## main code ##
            DFT_spectrum = self.get_DFT_spectrum(data_points)
            data_scale = np.mean(DFT_spectrum)
            spectrum_covariance_matrix = np.matrix(self.k_tools.get_kernel_array(spectral_covariance_function, 
                                                                                 x_range = frequency_range, 
                                                                                 y_range = frequency_range))
            nnls_results = optimize.nnls(A = spectrum_covariance_matrix, 
                                         b = np.array(DFT_spectrum).flatten())
            initial_spectral_weights = 0.1*np.reshape(nnls_results[0], newshape = (len(nnls_results[0]),1))
            spectral_weights = spectral_gradient_ascent(initial_spectral_weights,
                                                        number_iterations, 
                                                        learning_rate)
            return spectral_weights
        ## main code ##
        frequency_range = self.get_frequency_range(time)
        spectral_covariance_function =  self.covariance_functions.squared_exponential(length_scale = spectral_width)
        spectral_weights = get_spectral_weights(data_points)
        BFG_covariance = self.covariance_functions.generic_covariance()
        BFG_covariance.fourier = self.fun_tools.translated_linear_combination(bivariate_function = spectral_covariance_function, 
                                                                              weights_list = spectral_weights, 
                                                                              center_points = frequency_range)
        stationary_covariance = self.fun_tools.real(self.get_fourier_transform(kernel = spectral_covariance_function,
                                                           weights_list = spectral_weights,
                                                           center_points = frequency_range))
        BFG_covariance.function = self.fun_tools.bivariate_composition(lambda t1,t2: np.abs(t2 - t1), 
                                                                       stationary_covariance)
        return BFG_covariance
# 

class GP_regression_tools(object):
    #
    def __init__(self):
        self.description = "This class contains methods for working with GP regression"
        self.fun_tools = functional_tools()
        self.k_tools = kernel_tools()
        self.lin_tools = linear_tools()
        self.fou_tools = spectral_tools()
    #
    def get_cholesky_factor(self, 
                            kernel, 
                            data_range, 
                            noise_level):
        number_data_points = len(data_range)
        kernel_matrix = np.matrix(self.k_tools.get_kernel_array(kernel, 
                                                                x_range = data_range, 
                                                                y_range = data_range))
        data_covariance_matrix = kernel_matrix + noise_level**2*np.identity(number_data_points)
        cholesky_factor = np.linalg.cholesky(data_covariance_matrix)
        return cholesky_factor 
    #
    def get_GP_regression_weights_matrix(self, 
                                         cholesky_factor):
        identity = np.identity(cholesky_factor.shape[0])
        weights_matrix = self.lin_tools.matrix_division(divided = self.lin_tools.matrix_division(divided = identity, 
                                                                                                 divider = cholesky_factor, 
                                                                                                 side = "left", 
                                                                                                 cholesky = "no"),
                                                        divider = cholesky_factor.H,
                                                        side = "left", 
                                                        cholesky = "no")
                                                        
        return weights_matrix
    #
    def get_log_marginal_likelihood(self,
                                    cholesky_factor, 
                                    data_points):
        number_data_points = len(data_points)
        data_vector = np.matrix(np.reshape(data_points, 
                                           newshape=(number_data_points,1)))
        log_determinant = 2*np.sum(np.log(np.diagonal(cholesky_factor)))
        whitened_data = self.lin_tools.matrix_division(divided = data_vector, 
                                                       divider = cholesky_factor, 
                                                       side = "left", 
                                                       cholesky = "no")
        log_marginal_likelihood = -0.5*log_determinant - 0.5*float(whitened_data.T*whitened_data)
        return log_marginal_likelihood
    #
    def get_GP_regression_weights(self, 
                                  data_points, 
                                  weights_matrix):
        number_data_points = len(data_points)
        data_vector = np.matrix(np.reshape(data_points, 
                                           newshape=(number_data_points,1)))
        weights = weights_matrix*data_vector
        return np.array(weights).flatten()
    #
    def get_GP_regression_posterior(self, 
                                    data_points, 
                                    kernel, 
                                    data_range, 
                                    noise_level):
        cholesky_factor = self.get_cholesky_factor(kernel, 
                                                   data_range, 
                                                   noise_level)
        weights_matrix = self.get_GP_regression_weights_matrix(cholesky_factor)
        weights = self.get_GP_regression_weights(data_points, 
                                                 weights_matrix)
        expectation_function = self.fun_tools.translated_linear_combination(bivariate_function = kernel, 
                                                                            weights_list = weights, 
                                                                            center_points = data_range)
        covariance_correction = self.fun_tools.translated_quadratic_combination(bivariate_function = kernel, 
                                                                                weights_array = weights_matrix.tolist(), 
                                                                                first_center_points = data_range,
                                                                                second_center_points = data_range)
        covariance_function = self.fun_tools.bivariate_difference(kernel, 
                                                                  covariance_correction)
        variance_function = self.fun_tools.diagonal(covariance_function)
        fourier_transform = self.fou_tools.get_fourier_transform(kernel = kernel,
                                                                 weights_list = weights,
                                                                 center_points = data_range)
        log_marginal_likelihood = self.get_log_marginal_likelihood(cholesky_factor, 
                                                                   data_points)
        results = {"expectation": expectation_function, 
                   "covariance": covariance_function,
                   "variance": variance_function,
                   "second_moment": self.fun_tools.sum(variance_function,
                                                       self.fun_tools.power(expectation_function,2)),
                   "pdf": self.fun_tools.gaussian_family(mu_function = expectation_function, 
                                                         var_function = variance_function),
                   "log_ML": log_marginal_likelihood,
                   "fourier": fourier_transform}
        return results
    #
    def multiple_GP_analysis(self, 
                             data_points, 
                             kernels_list, 
                             data_range, 
                             noise_level):
        GP_regression_posterior = self.get_GP_regression_posterior(data_points, 
                                                                   kernels_list[-1], 
                                                                   data_range, 
                                                                   noise_level)
        if len(kernels_list) == 1:
            GP_posteriors_list = [GP_regression_posterior]
        else:
            GP_posteriors_list = (self.multiple_GP_analysis(data_points, 
                                                            kernels_list[:-1], 
                                                            data_range, 
                                                            noise_level) 
                                  + [GP_regression_posterior])
        return GP_posteriors_list
    #
    def meta_GP_analysis(self, GP_posteriors_list):
        ## private functions ##
        def get_probabilities(log_likelihoods):
            alpha = np.min(log_likelihoods)
            nonNormalized_probabilities = np.exp(log_likelihoods - alpha)
            return nonNormalized_probabilities/np.sum(nonNormalized_probabilities)
        #
        def get_optimal_result(results_list, probabilities):
            optimal_kernel_index = np.argmax(probabilities)
            return results_list[optimal_kernel_index]
        ## main code ##
        log_likelihoods = np.array([result["log_ML"] for result in GP_posteriors_list])
        kernel_probabilities = get_probabilities(log_likelihoods)
        optimal_result = get_optimal_result(GP_posteriors_list, kernel_probabilities)
        expectations_list = [result["expectation"] for result in GP_posteriors_list]
        fourier_list = [result["fourier"] for result in GP_posteriors_list]
        second_moments_list = [result["second_moment"] for result in GP_posteriors_list]
        pdf_list = [result["pdf"] for result in GP_posteriors_list]
        marginalized_expectation = self.fun_tools.linear_combination(expectations_list, 
                                                                     kernel_probabilities.tolist())
        marginalized_second_moment = self.fun_tools.linear_combination(second_moments_list, 
                                                                       kernel_probabilities.tolist())
        marginalized_variance = self.fun_tools.difference(marginalized_second_moment,
                                                          self.fun_tools.power(marginalized_expectation,2))
        marginalized_pdf = self.fun_tools.bivariate_linear_combination(pdf_list, 
                                                                       kernel_probabilities.tolist())
        marginalized_fourier = self.fun_tools.linear_combination(fourier_list, 
                                                                 kernel_probabilities.tolist())
        return {"probabilities": kernel_probabilities,
                "optimized": optimal_result,
                "marginalized": {"expectation": marginalized_expectation, 
                                 "variance": marginalized_variance,
                                 "pdf": marginalized_pdf,
                                 "fourier": marginalized_fourier}}
    #
    def plot_GP_posterior(self,
                          GP_posterior_expectation, 
                          GP_posterior_variance,
                          target_range):
        expectation = GP_posterior_expectation(target_range)
        error_bars = np.sqrt(GP_posterior_variance(target_range))
        upper_bar = expectation + error_bars
        lower_bar = expectation - error_bars
        plt.plot(target_range, expectation, c = "r", lw = 2, ls = "--", label = "Expected value")
        plt.fill_between(target_range, lower_bar, upper_bar, alpha = 0.4, color = "r", label = "Standard deviation")
        plt.title("GP analysis")
        plt.legend(loc = "best")
        plt.xlim(min(target_range),max(target_range))
        return
    # 
    def plot_posterior_pdf(self, GP_pdf, value_range, target_range):
        from matplotlib.colors import LogNorm
        mesh_1, mesh_2 = np.meshgrid(value_range, target_range)
        pdf_array = GP_pdf(mesh_1, mesh_2)
        plt.imshow(np.transpose(pdf_array), 
                   aspect='auto',
                   origin='lower',
                   norm=LogNorm(vmin=0.001, vmax=25),
                   extent=(min(target_range),max(target_range), min(value_range),max(value_range)))
        plt.title("Marginal posterior densities")
        plt.xlim(min(target_range),max(target_range))
        plt.colorbar()
        return

