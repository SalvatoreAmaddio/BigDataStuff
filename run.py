from MySparql import data
import pandas as pd

data = pd.DataFrame(data)

#filter data to select Scotland only 
#as the file might come with a further background per regions of Scotland
scotland_data = data[data['Reference Area'] == 'Scotland']

#ensure data are ordered by Year in Ascending order
scotland_data = scotland_data.sort_values(by=["Reference Period"], ascending=[True])

#select only the rows where Sex = All and Measure Type is not 95% upper or lower confidence limit 
filtered_data = scotland_data[
    (data['Sex'] == 'All') &
    ~data['Measure Type'].str.contains('confidence limit', case=False, na=False)
]

##ANALYSE DATA ABOUT SMOKING AND E-CIGARETS
#select only data where Indicator is relevant to smoking and vaping
smoke_data = filtered_data[
                filtered_data['Indicator'].str.contains('smok', case=False, na=False)
                | filtered_data['Indicator'].str.contains('E-cig', case=False, na=False)
            ]

#group by 'Reference Period', 'Indicator', 'Sex', 'Measure Type'
grouped_data = smoke_data.groupby(['Reference Period', 'Indicator', 'Sex', 'Measure Type']).agg({'Value': 'first'}).reset_index()

#select only 'Reference Period', 'Indicator',"Value"
grouped_data = grouped_data[['Reference Period', 'Indicator',"Value"]]

#make a pivot table for a better overview
pivot_table = grouped_data.pivot_table(
    index='Reference Period', 
    columns='Indicator', 
    values='Value',
    aggfunc='first'
)

#Reset the index to display the Reference Period column
pivot_table.reset_index(inplace=True)

#Rename columns in a friendly and shorter way
pivot_table = pivot_table.rename(columns={
    'Reference Period' : 'Year',
    'Smoking status: Current smoker': 'Smokers',
    'Smoking status: Never smoked/Used to smoke occasionally': 'Never or Occasional Smoker',
    'Smoking status: Used to smoke regularly': 'Former Smoker',
    'E-cigarette use: Currently using': 'Vapers',
    'E-cigarette use: Ever previously used': 'Vaped at least once',
    'E-cigarette use: Never used': 'Never Vaped',
})

pivot_table.to_csv('file_grouped.csv', index=False)
