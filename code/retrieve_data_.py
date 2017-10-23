import argparse, requests, json

def get_data(userid, datefrom, dateto, output_file, typeAnalysis):
    """ This function gets a date in the format of YYYY-MM-DD and an output
    file, queries the given API and then writes the results of the queries to
    the output
    
    Parameters
    ----------
    date: string
        A date in the format YYYY-MM-DD.
    output_file: string
        An output file to write the data to.
    
    """
    auth = ('lipcsikgy@gmail.com', '123456789')
    
    if(typeAnalysis=="Event"):
        r = requests.get(
                'http://ditaapi.azurewebsites.net/Event/' + userid + '/' + datefrom + '/' + dateto,
                auth=auth
                )
        try:
            with open(output_file, 'w') as f:
                f.write(json.dumps(r.json(), sort_keys=True, indent=4))
                return 1
        except ValueError:
            return 0
    elif(typeAnalysis=="ABD"):
        r = requests.get(
                'http://ditaapi.azurewebsites.net/ABD/' + userid + '/' + datefrom + '/' + dateto,
                auth=auth
                )
        try:
            with open(output_file, 'w') as f:
                f.write(json.dumps(r.json(), sort_keys=True, indent=4))
                return 1
        except ValueError:
            return 0
        
def get_dataABD(date_from, date_to, output_file):
    """ This function gets a date in the format of YYYY-MM-DD and an output
    file, queries the given API and then writes the results of the queries to
    the output
    
    Parameters
    ----------
    date: string
        A date in the format YYYY-MM-DD.
    output_file: string
        An output file to write the data to.
    
    """
    auth = ('lipcsikgy@gmail.com', '123456789')
    r = requests.get(
            'http://ditaapi.azurewebsites.net/ABD/' + date_from + '/' + date_to,
            auth=auth
            )

    try:
        with open(output_file, 'w') as f:
            f.write(json.dumps(r.json(), sort_keys=True, indent=4))
            return 1
    except ValueError:
        return 0    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "typeAnalysis",
            type=str,
            help="Specify the type of analysis: either ABD or Event"
            )
    parser.add_argument(
            "output_file",
            type = str,
            help="Specify the name of the output file. If it's not specified \
                output.txt will be used"
            )
    parser.add_argument(
        "dateto",
        type=str,
        help="The date to which you want to query records (format YYYY-MM-DD)"
        )
    parser.add_argument(
        "datefrom",
        type=str,
        help="The date from which you want to query records (format YYYY-MM-DD)"
        )
    parser.add_argument(
        "userid",
        type=str,
        help="The user id for which you want to query records"
        )
    args = parser.parse_args()
    print args.typeAnalysis
    get_data(args.typeAnalysis,args.userid,args.datefrom,args.dateto, args.output_file)
    