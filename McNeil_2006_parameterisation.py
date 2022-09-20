# -*- coding: utf-8 -*-
"""
Created on Sat May  7 09:24:05 2022
This is an implementation of McNeil et.al 2006.

McNeil, C.L., and E.A. D'Asaro, 
Parameterization of air-sea gas exchange at extreme wind speeds, 
Journal of Marine Systems, 66, 110-121, 2007.
https://doi.org/10.1016/j.jmarsys.2006.05.013

https://www.sciencedirect.com/science/article/pii/S0924796306001771


Important note: This parameterisation raises wind speed to a power of 3.742.
This means that to capture the variability in the wind speed as we do by taking the
second moment of the wind e.g <u10>^2 for other parameterisations. It is necessary 
to calculate the moment to this power for all wind speed measurements beforehand 
and you must pass that as an input in the configuration file.
e.g. <u10>^3.742. Here this variables is crudely called windu10_moment_3_742

Import note 2: This parameterisation is only suitable at high wind speeds!
Additionally this parameterisation does not pass through 0.
Therefore it will give inaccurate results at low to medium wind speeds.
If this parameterisation must be used, it should be used with extreme caution
especially for wind speeds below 20 ms-1. 

@author: rps207
"""

#McNeil 2006
class k_McNeil2006(KCalculationBase):
    def __init__(self):
        self.name = self.__class__.__name__;
    
    def input_names(self):
        return ["windu10", "windu10_moment2","windu10_moment_3_742", "scskin"];
        
    def output_names(self):
        return ["k"];
    
    def __call__(self, data):
        function = "(rate_parameterisation.py: k_McNeil2006.__call__)";
        print("%s Using the McNeil et al., 2006 (Mc06) k parameterisation" % (function))
        try:
            #for ease of access, simply assign attributes to each input/output.
            for name in self.input_names() + self.output_names():
                setattr(self, name, data[name].fdata);
            data["k"].standardName="gas_transfer_velocity_of_carbon_dioxide" ;
            data["k"].longName="McNeil et al., 2006 (Mc06) gas transfer velocity";
        except KeyError as e:
            print("%s: Required data layer for selected k parameterisation was not found." % function);
            print(type(e), e.args);
            return False;
        
        #determine the McNeil et al., 2006  k relationship
        for i in arange(len(self.k)):   
            self.k[i] = DataLayer.missing_value
            if ( (self.windu10[i] != DataLayer.missing_value) and (self.windu10_moment2[i] != DataLayer.missing_value) and (self.windu10_moment_3_742[i] != DataLayer.missing_value)and (self.scskin[i] != DataLayer.missing_value) and (self.scskin[i] > 0.0) ):#SOCATv4 - No need for wind moment3
                # We advise calculating the moment to a power 3.742
                # However it should be noted that the two following 
                # two lines of code can be uncommented and commented
                # if this is not possible.
                
                #self.k[i] = 14+(0.0002925*((self.windu10[i])**3.742)); 
                self.k[i] = 14+(0.0002925*(self.windu10_moment_3_742[i])); 
                
                
                self.k[i] = self.k[i] * sqrt(600.0/self.scskin[i])
            else:
                self.k[i] = DataLayer.missing_value
        
        return True;


