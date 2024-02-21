class Number():
    def __init__(self,string):
        
        #formatting to make sure everything is consisten
        if '.' not in string:
            string += "."
        if string[0].isdigit():
            string = "+"+string
        elif string[0]=='.':
            string = "+0"+string
        elif string[0:2] =="-.":
            string.replace("-.","-0.") 
        string = string.strip("0")
        self.sign = string[0]
        self.integer,self.mantissa = string[1:].split('.')
    
    def copy(self):
        return Number(self.__str__())
    def __str__(self):
        return self.sign + self.integer+ "." +self.mantissa
    def __neg__(self):
        sign = "+" if self.sign != "+" else "-"
        return Number(sign + self.integer + "." + self.mantissa)
    def __abs__(self):
        return Number("+" + self.integer + "." + self.mantissa) 
    
    def __eq__(self, other_number):
        return self.__str__() == other_number.__str__()
    def __ne__(self, other_number):
        return not self.__eq__(other_number)
    def __gt__(self,other_number):
        if self.sign ==other_number.sign:
            n = self - other_number
            if n == Number('0'):
                return False
            elif n.sign == self.sign:
                return self.sign == "+"
            elif n.sign != self.sign:
                return self.sign == "-"
        else:
            return self.sign == "+" # this is reversed because of where "+" and "-" are naturally sorted
        
    def __lt__(self,other_number):
        if self.sign ==other_number.sign:
            n = self - other_number
            if n == Number('0'):
                return False
            elif n.sign == self.sign:
                return self.sign == "-"
            elif n.sign != self.sign:
                return self.sign == "+"
        else:
            return self.sign == "-" # this is reversed because of where "+" and "-" are naturally sorted
    
    def __le__(self,other_number):
        return self == other_number or self < other_number
    
    def __ge__(self,other_number):
        return self == other_number or self > other_number
    
    def __add__(self,other_number):
        if self.sign == other_number.sign:
            #makes sure mantissa are same length
            max_mantissa = max(len(self.mantissa),len(other_number.mantissa))
            m1 = self.mantissa.ljust(max_mantissa,'0')
            m2 = other_number.mantissa.ljust(max_mantissa,'0')
            
            #makes sure integer are same length plus and extra zero for carry
            max_integer = max(len(self.integer),len(other_number.integer))
            i1 = self.integer.rjust(max_integer + 1,'0')
            i2 = other_number.integer.rjust(max_integer + 1,'0')
            
            #combines them into one big number.
            c1 = i1+m1
            c2 = i2+m2
            
            solution = ""
            
            #go in reverse through string doing addition
            carry = 0 # this is the amount we need to carry each time
            for count , index in enumerate(range(len(c1)-1,-1,-1)):
                if count == max_mantissa:
                    solution += '.'
                
                v1 = int(c1[index])
                v2 = int(c2[index])
                value = v1+v2
                value += carry
                
                carry = int(value/10)
                value %= 10
                
                solution += str(value)
            
            #flip solution
            solution = solution[::-1]
            #string leading and trailing zeros
            solution = solution.strip("0")
            #replace sign
            solution = self.sign + solution
            
            return Number(solution)
        else:
            return self -(-other_number)
            
        
    def __sub__(self,other_number):
        if self.sign == other_number.sign:
            #makes sure mantissa are same length
            max_mantissa = max(len(self.mantissa),len(other_number.mantissa))
            m1 = self.mantissa.ljust(max_mantissa,'0')
            m2 = other_number.mantissa.ljust(max_mantissa,'0')
            
            #makes sure integer are same length plus and extra zero for carry
            max_integer = max(len(self.integer),len(other_number.integer))
            i1 = self.integer.rjust(max_integer+1,'0')
            i2 = other_number.integer.rjust(max_integer+1,'0')
            
            #combines them into one big number.
            c1 = i1+m1
            c2 = i2+m2
            
            #figure out which is larger
            larger = max(c1,c2)
            smaller = min(c1,c2)
            
            solution = ""
            
            steal = 0 # this is the amount we need to carry each time
            for count , index in enumerate(range(len(c1)-1,-1,-1)):
                if count == max_mantissa:
                    solution += '.'
                
                v1 = int(larger[index])
                v2 = int(smaller[index])
                
                if steal == -1 and v1 == 0:
                    steal =-1
                    v1 = 9
                elif v1<v2:
                    steal = -1
                    v1+=10
                else:
                    v1+=steal
                    steal = 0
                
                value = v1-v2
                solution += str(value)
                
            #flip solution
            solution = solution[::-1]
            #string leading and trailing zeros
            solution = solution.strip("0")
            #replace sign
            if c1 == larger:
                solution = self.sign + solution
            else:
                solution = ("+" if self.sign != "+" else "-")+solution
            
            return Number(solution)
        else:
            return self +(-other_number)
            
    def __mul__(self,other_number):
        #makes sure mantissa are same length
        max_mantissa = max(len(self.mantissa),len(other_number.mantissa))
        m1 = self.mantissa.ljust(max_mantissa,'0')
        m2 = other_number.mantissa.ljust(max_mantissa,'0')

        #makes sure integer are same length plus and extra zero for carry
        max_integer = max(len(self.integer),len(other_number.integer))
        i1 = self.integer.rjust(max_integer+1,'0')
        i2 = other_number.integer.rjust(max_integer+1,'0')

        #combines them into one big number.
        c1 = i1+m1
        c2 = i2+m2
        
        final_solution = Number("0")
            
        
        for count_2 , index_2 in enumerate(range(len(c2)-1,-1,-1)):
            partial_solution = ""+("0"*count_2)
            digit_2 = c2[index_2]
            carry = 0
            for count_1 , index_1 in enumerate(range(len(c1)-1,-1,-1)):
                if len(partial_solution) == max_mantissa *2 :
                    partial_solution += '.'
                    pass
                
                digit_1 = c1[index_1]
                value = int(digit_1)*int(digit_2) + carry
                
                carry = int(value/10)
                value %= 10
                partial_solution += str(value)
            #flip solution
            partial_solution = partial_solution[::-1]
            #string leading and trailing zeros
            partial_solution = partial_solution.strip("0")
            #replace sign
            if self.sign == other_number.sign:
                partial_solution = '+' + partial_solution
            else:
                partial_solution = '-' +partial_solution 
            final_solution = final_solution + Number(partial_solution)
        return final_solution
    def __truediv__(self,other_number):
        print('DIV')
