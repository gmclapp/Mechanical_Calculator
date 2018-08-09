import sanitize_inputs as si
import database_functions as df

##class material:
##    def __init__(self, name, E=None, YTS=None, UTS=None, density=None, tc=None, tcexp=None):
##        self.name = name
##        self.elastic_modulus = E
##        self.YTS = YTS
##        self.UTS = UTS
##        self.density = density
##        self.thermal_conductivity = tc
##        self.therm_coef_exp = tcexp
    
def calc_cross_area(shape, height, width, OD, wall):
    if shape.lower() == 'r':
        area = width*height
        if wall != 0:
            area -= (width-2*wall)*(height-2*wall)

    elif shape.lower() == 'c':
        area = math.pi*(OD**2)/4
        print("Solid area = ", area)
        if wall != 0:
            area -= math.pi*((OD/2)-wall)**2

    return(area)

def calc_mom_inertia(shape, height, width, OD, wall):
    if shape.lower() == 'r':
        Ixx = (width*height**3) / 12
        if wall != 0:
            Ixx -= (width-2*wall)*(height-2*wall)**3/12
        
    elif shape.lower() == 'c':
        Ixx = (math.pi/4)*(OD/2)**4
        if wall != 0:
            Ixx -= (math.pi/4)*((OD/2)-wall)**4

    return(Ixx)

yes_no = ['y','n','Y','N']
acceptable_units = ['e', 'm', 'E', 'M']
units = si.get_letter("(E)nglish or (M)etric?", acceptable_units)

height = 0
width = 0
wall = 0
OD = 0
area = 0

rfile = open("Materials.csv",'r')
headers = df.list_headers(rfile, 'r')
material_list = []

##for i in range(len(headers)):
##    material_list.append(headers[i], df.vlookup(rfile, headers[i], 0, 1))

if units.lower() == 'e':
    length_units = "in"
    force_units = "lbf"
    mass_units = "slugs"
    
elif units.lower() == 'm':
    length_units = "mm"
    force_units = "N"
    mass_units = "kg"
    
else:
    print("Units error.")

acceptable_shapes = ['c','r','C','R']
shape = si.get_letter("(R)ectangular or (C)ylindrical cross-section")
tube = si.get_letter("Hollow tube? (y/n)")

if shape.lower() == 'r':
    hgt_prompt = "Enter the height of the cross-section (" + length_units + ")"
    height = si.get_real_number(hgt_prompt, positive = True, negative = False)

    wid_prompt = "Enter the width of the cross-section (" + length_units + ")"
    height = si.get_real_number(wid_prompt, positive = True, negative = False)

elif shape.lower() == 'c':
    OD_prompt = "Enter the outer diameter of the cross-section (" + length_units + ")"
    OD = si.get_real_number(OD_prompt, positive = True, negative = False)

if tube == 'y':
    wall_prompt = "Enter the wall thickness of the cross-section (" + length_units + ")"
    wall = si.get_real_number(wall_prompt, positive = True, negative = False)

area = calc_cross_area(shape, height, width, OD, wall)

acceptable_loading = ['c','o','t','s','C','O','T','S']
print("Enter the loading configuration.")
loading_configuration = si.get_letter(
    "(C)antilever\nC(o)mpression\n(T)ension\n(S)hear\n>>>", acceptable_loading)

len_prompt = "Enter the length of the part (" + length_units + ")"
length = si.get_real_number(len_prompt, positive = True, negative = False)

force_prompt = "Enter the force applied. (" + force_units + ")"
force = si.get_real_number(force_prompt)

