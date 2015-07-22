from matplotlib import rc
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import xlabel, ylabel
from global_values import OUTPUT_DIR

class Plotter(object):
    '''
    Plotter class is a static class to draw and save png/pdf images of 
    the x-y array values with size values.
    '''

    @staticmethod
    def scatter(title, file_name, x_array, y_array, size_array, x_label, \
                y_label, x_range, y_range, print_pdf):
        '''
        Plots the given x value array and y value array with the specified 
        title and saves with the specified file name. The size of points on
        the map are proportional to the values given in size_array. If 
        print_pdf value is 1, the image is also written to pdf file. 
        Otherwise it is only written to png file.
        '''
        rc('text', usetex=True)
        rc('font', family='serif')
        plt.clf() # clear the ploting window, a must.                               
        plt.scatter(x_array, y_array, s =  size_array, c = 'b', marker = 'o', alpha = 0.4)
        if x_label != None:   
            plt.xlabel(x_label)
        if y_label != None:
            plt.ylabel(y_label)                
        plt.axis ([0, x_range, 0, y_range])
        plt.grid(True)
        plt.suptitle(title)
    
        Plotter.print_to_png(plt, file_name)
        
        if print_pdf:
            Plotter.print_to_pdf(plt, file_name)
        
    @staticmethod    
    def print_to_png(image, file_name):
        '''
        Creates a png image file with specified file name and 
        specified image.
        '''
        output = OUTPUT_DIR + file_name + '.png'
        plt.savefig(output)
    
    @staticmethod
    def print_to_pdf(image, file_name):
        '''
        Creates a pdf image file with specified file name and 
        specified image.
        '''
        output = OUTPUT_DIR + file_name + '.pdf'
        pdf_file = PdfPages(output)
        plt.savefig(pdf_file, format='pdf')
        pdf_file.close()
    
