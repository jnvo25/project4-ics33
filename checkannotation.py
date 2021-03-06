# Submitter: juliethl (Lai, Juliette)
# Partner: jonatnv1 (Vo, Jonathan)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # We start by binding the class attribute to True meaning checking can occur
    #   (but only when the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # For checking the decorated function, bind its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursiv
        # We start by comparing check's function annotation to its arguments
#         print("Annotation: ", annot, annot == list, isinstance(annot, list))
        
        def checkList(self):
            # if value is not a list raise error
            if not isinstance(value, list):
                raise AssertionError(f"""'{param}' failed annotaion check(wrong type): value = {value}
    was type {type_as_str(value)} ...should be type list""")
            
            # check for consistency if annot is 1 element
            if len(annot) == 1:
                annot_type = annot[0]
                for index, element in enumerate(value):
                    local_check_history = f"list[{index}] check: {annot_type}\n"
                    self.check(param, annot_type, element, check_history+local_check_history)
                    
            # check for equality for both
            else:
                if len(annot) != len(value):
                    raise AssertionError(f"""'{param}' failed annotaion check(wrong number of elements): value = {value}
    annotation had {len(annot)} elements{annot}
    {check_history}""")
                for index in range(len(value)):
                    local_check_history = f"list[{index}] check: {annot[index]}\n"
                    self.check(param, annot[index], value[index], check_history+local_check_history)
                    

        def checkTuple(self):
            if not isinstance(value, tuple):
                raise AssertionError(f"""'{param}' failed annotaion check(wrong type): value = {value}
    was type {type_as_str(value)} ...should be type tuple""")
                
            if len(annot) == 1:
                annot_type = annot[0]
                for element in value:
                    local_check_history = f"list[{element}] check: {annot_type}\n"
                    self.check(param, annot_type, element, check_history+local_check_history)
            ## need to add to check_history
            
            else:
                if len(annot) != len(value):
                    raise AssertionError(f"""'{param}' failed annotaion check(wrong number of elements): value = {value}
    annotation had {len(annot)} elements{annot}
    {check_history}""")
                for index in range(len(value)):
                    local_check_history = f"list[{index}] check: {annot[index]}\n"
                    self.check(param, annot[index], value[index], check_history+local_check_history) 
            
        def checkDict(self):
            if not isinstance(value, dict):
                raise AssertionError(f"""'{param}' failed annotation check(wrong type): value = {value}
    was type {type_as_str(value)} ...should be type dict""")
            
            if len(annot) != 1:
                raise AssertionError(f"""'{param}' annotation inconsistency: set should have 1 value but had {len(annot)}
    annotation = {annot}""")
            else:
                annot_key = list(annot.keys())[0]
                for key in value.keys():
                    local_check_history = f"dict key check: {annot_key}\n"
                    self.check(param, annot_key, key, check_history+local_check_history)
                    
                annot_value = list(annot.values())[0]
                for v in value.values():
                    local_check_history = f"dict value check: {annot_value}\n"
                    self.check(param, annot_value, v, check_history+local_check_history)
        
        def checkSet(self):
            if len(annot) != 1:
                raise AssertionError(f"""'{param}' annotation inconsistency: {annot} should have 1 value but had {len(annot)}
    annotation = {annot}""")
            else:
                for element in value:
                    local_check_history = f"set value check: {list(annot)[0]}\n"
                    self.check(param, list(annot)[0], element, check_history+local_check_history)

        
            
        
        if annot == None:
            pass
        
        
        elif isinstance(annot, type):
            if not isinstance(value, annot):
                raise AssertionError(f"""'{param}' failed annotation check(wrong type): value = '{value}'
    was type {type_as_str(value)} ...should be type {annot}
    {check_history}""")
                
                
        elif isinstance(annot, list):
            checkList(self)
        
        elif isinstance(annot, tuple):
            checkTuple(self)
            
        elif isinstance(annot, dict):
            checkDict(self) 
            
        elif isinstance(annot, set):
            if not isinstance(value, set):
                raise AssertionError(f"""'{param}' failed annotation check(wrong type): value = {value}
    was type {type_as_str(value)} ...should be type set""")
            checkSet(self)            
        
        elif isinstance(annot, frozenset):
            if not isinstance(value, frozenset):
                raise AssertionError(f"""'{param}' failed annotation check(wrong type): value = {value}
    was type {type_as_str(value)} ...should be type frozenset""")
            checkSet(self)
                        
        elif inspect.isfunction(annot):
            if len( annot.__code__.co_varnames) != 1:
                raise AssertionError(f"""'{param}' annotation inconsistency: predicate should have 1 parameter but had {len( annot.__code__.co_varnames)}
    predicate = {annot}""")


            if isinstance(value, list):
                for index, element in enumerate(value):
                    local_check_history = f"list[{index}] check: {annot}\n"
                    self.check(param, annot, element, check_history+local_check_history)
            else:
                try:
                    x = annot(value)
                except Exception as exception:
                    raise AssertionError(f"""'{param}' annotation predicate({annot}) raised exception
    exception = {type(exception).__name__}: {exception}\n{check_history}""")
                if not x:
                    raise AssertionError(f"""'{param}' failed annotation check: value = {value}
    predicate = {annot}\n{check_history}""")

            
            try:
                x = annot(value)
            except Exception as exception:
                raise AssertionError(f''''{param}' annotation predicate{annot} raised exception
    exception = {exception}''')
            if not x:
                raise AssertionError(f"""'{param}' failed annotation check: value = {value}
    predicate = {annot}""") 

                
        else:
            flag = False
            try:
                annot.__check_annotation__(self, check, param, value, check_history)
            except AttributeError:
                # Skip next except to raise special assertion
                flag = True
            except Exception as e:
                #  program raises exception
                raise AssertionError(f"""'{param}' annotation {value} raised exception
    exception = {e}
    {check_history}""")

            # Special assertion for attributition error
            if flag:
                raise AssertionError(f"""'{param}' annotation undecipherable: {value}\n{check_history}""")
        
            if not isinstance(value, annot):
                raise AssertionError(f"""'{param}' failed annotation check(wrong type): value = {value}
    was type {type(value)} ...should be type {annot}""")
            
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Returns the parameter->argument bindings as an ordereddict, derived
        #   from dict, binding the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        if not (self.checking_on and self._checking_on):
            return self._f(*args, **kargs)
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        try:
            # Check the annotation for each of the annotated parameters
            arguments = param_arg_bindings()
            annots = self._f.__annotations__
#             print(arguments, annots)
            for param, value in arguments.items():
                if param in annots:
                    annot = annots[param]
                    self.check(param, annot, value)
            
            # Compute/remember the value of the decorated function
            value = self._f(*args, **kargs)
            # If 'return' is in the annotation, check it
            if 'return' in annots:
                self.check('return', annots['return'], value)
            # Return the decorated answer
            return value
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
#             print(80*'-')
#             for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
#                 print(l.rstrip())
#             print(80*'-')
            raise



  
if __name__ == '__main__':     
    # an example of testing a simple annotation  

    def f(x:[str]): pass
    f = Check_Annotation(f)
    f([1,'a'])

           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4W20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()