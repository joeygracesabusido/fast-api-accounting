from database import Database
Database.initialize()


def autocomplete_surigao():

    # items = chartofAccounts(mydb.chart_of_account.find({'accountTitle':{"$regex":term,'$options':'i'}}))

    # suggestions = []
    # for item in items:
    #     suggestions.append(item['accountTitle'])
    # return suggestions
    term = input("Enter Equipment: ")
   
    equipmentResult = Database.select_equipment(id=term)
    for i in equipmentResult:
        equipmentID = i[1]
   
    # agg_result_list_eqp = []
    # for x in equipmentResult:
        
    #     equipment_id = x[1]

    #     data={}   
        
    #     data.update({
           
    #         'equipment_id': equipment_id,
            
    #     })

    #     agg_result_list_eqp.append(data)
        print(equipmentID)

autocomplete_surigao()