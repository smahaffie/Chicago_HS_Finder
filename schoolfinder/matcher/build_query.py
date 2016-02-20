neighbors = """find_neighborhood_schools("{}", address)""".format(str(form.cleaned_data['your_address']))

"""SELECT main.name, main.school_type, act.composite_score_mean, fot.fot, main.rating 
FROM main JOIN fot JOIN act JOIN cep JOIN addrs ON main.school_id = fot.school_id AND 
main.school_id = act.school_id AND main.school_id = cep.school_id AND addrs.school_id = main.school_id 
WHERE main.school_type IN ("Selective Enrollment","Magnet","Contract","Options","Reinvestment", "Charter") 
OR main.school_type = "Neighborhood" AND main.school_id IN (SELECT * FROM main JOIN addrs ON addrs.school_id = main.school_id WHERE """ + neighbors + ");"




"""