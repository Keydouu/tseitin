return tseitin of a logical formula.
Usage: python script.py <input_string>
examples :

> python formulaReader.py "!p"

tseitin(!p) = ( Yns, (Yns|p)&(!Yns|!p))

> python formulaReader.py "p&r"

tseitin(p&r) = ( Yns, (Yns|!p|!r)&(!Yns|p)&(!Yns|r))

> python formulaReader.py "(p&r)|(!p|!r)"
tseitin((p&r)|(!p|!r)) = ( Yns, Yns)

Warning: no variables in this model (and so, no generated file)!

> python formulaReader.py "p<=>(p&r)"

tseitin(p<=>(p&r)) = ( Yns, (Yns|!r)&(Yns|p)&(!Yns|r|!p))
