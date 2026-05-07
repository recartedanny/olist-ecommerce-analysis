import pandas


def clean_data(datasets):

    for name,df in datasets.items():
        if name== "geolocation":
            df.drop_duplicates(subset='geolocation_zip_code_prefix',
                                    keep='first', 
                                    inplace=True,            
                                    ignore_index=True )

    return datasets