print(
    #changes directory to the directory of this file
    (os:=__import__('os')) 
    and (np:=__import__('numpy')) 
    and os.chdir(os.path.dirname(os.path.realpath(__file__))) 
    or '',
    #solution
    *[np.sum(
        np.arange(0, t_max).astype(np.int64) 
        * (t_max - np.arange(0, t_max).astype(np.int64)) 
        > d_record
        ) for t_max,d_record in zip(
            *(
                eval("_".join(line[9:].split())+',') 
                for line in open("records.txt", "r").read().splitlines()
              )
            )
        ],
    sep=''
    )