import bpy

nodes = [node.bl_rna.name for node in bpy.types.ShaderNode.__subclasses__()]

nodeID = [node.bl_rna.identifier for node in bpy.types.ShaderNode.__subclasses__()]


math_ops = ["Add Math", "Subtract Math", "Multiply Math", "Divide Math", "Multiply Add Math", "Power Math", "Logarithm Math", "Square Root Math", 
"Inverse Square Root Math", "Absolute Math", "Exponent Math", "Minimum Math", "Maximum Math", "Less Than Math", "Greater Than Math", "Sign Math", 
"Compare Math", "Smooth Minimum Math", "Smooth Maximum Math", "Round Math", "Floor Math", "Ceiling Math", "Truncate Math", "Fraction Math", 
"Modulo Math", "Wrap Math", "Snap Math", "Ping Pong Math", "Sine Math", "Cosine Math", "Tangent Math", "Arcsine Math", "Arccosine Math", "Arctangent Math", 
"Arctan2 Math", "Hyperbolic Sine Math", "Hyperbolic Cosine Math", "Hyperbolic Tangent Math", "To Radians Math", "To Degrees Math"]
math_ops_id = ["ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "MULTIPLY_ADD", "POWER", "LOGARITHM", "SQRT", "INVERSE_SQRT", "ABSOLUTE", "EXPONENT", "MINIMUM", 
"MAXIMUM", "LESS_THAN", "GREATER_THAN", "SIGN", "COMPARE", "SMOOTH_MIN", "SMOOTH_MAX", "ROUND", "FLOOR", "CEIL", "TRUNC", "FRACT", "MODULO", "WRAP", "SNAP", 
"PINGPONG", "SINE", "COSINE", "TANGENT", "ARCSINE", "ARCCOSINE", "ARCTANGENT", "ARCTAN2", "SINH", "COSH", "TANH", "RADIANS", "DEGREES"]


vector_math_ops = ["Add Vector Math", "Subtract Vector Math", "Multiply Vector Math", "Divide Vector Math", "Cross Product Vector Math", "Project Vector Math", 
"Reflect Vector Math", "Dot Product Vector Math", "Distance Vector Math", "Length Vector Math", "Scale Vector Math", "Normalize Vector Math", "Absolute Vector Math", 
"Minimum Vector Math", "Maximum Vector Math", "Floor Vector Math", "Ceiling Vector Math", "Fraction Vector Math", "Modulo Vector Math", "Wrap Vector Math", "Snap Vector Math",
"Sine Vector Math", "Cosine Vector Math", "Tangent Vector Math"]
vector_math_ops_id = ["ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "CROSS_PRODUCT", "PROJECT", "REFLECT", "DOT_PRODUCT", "DISTANCE", "LENGTH", "SCALE", "NORMALIZE", "ABSOLUTE", 
"MINIMUM", "MAXIMUM", "FLOOR", "CEIL", "FRACTION", "MODULO", "WRAP", "SNAP", "SINE", "COSINE", "TANGENT"]


mixrgb_ops = ["Mix Color", "Darken Color", "Multiply Color", "Burn Color", "Lighten Color", "Screen Color", "Dodge Color", "Add Color", "Overlay Color", "Soft Light Color", 
"Linear Light Color", "Difference Color", "Subtract Color", "Divide Color", "Hue Color", "Saturation Color", "Color", "Value Color"]
mixrgb_ops_id = ["MIX", "DARKEN", "MULTIPLY", "BURN", "LIGHTEN", "SCREEN", "DODGE", "ADD", "OVERLAY", "SOFT_LIGHT", "LINEAR_LIGHT", "DIFFERENCE", "SUBTRACT", "DIVIDE", 
"HUE", "SATURATION", "COLOR", "VALUE"]


node_names = nodes + math_ops + vector_math_ops + mixrgb_ops
node_id = nodeID + math_ops_id + vector_math_ops_id + mixrgb_ops_id

node_dir = {node_names[i]: node_id[i] for i in range(len(node_names))}

icon_list = ['left', 'right', 'down', 'up', 'up-left', 'up-right', 'down-left', 'down-right']