"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import pandas as pd
    import zipfile
    import os
    import warnings
    warnings.filterwarnings('ignore')

    #
    # Lectura de datos
    #
    file_names = os.listdir('files/input/')

    for i, file in enumerate(file_names):
        with zipfile.ZipFile(f'files/input/{file}', 'r') as z:
            with z.open(f'bank_marketing_{i}.csv') as f:
                if i == 0:
                    df = pd.read_csv(f)
                else:
                    df = pd.concat([df, pd.read_csv(f)])
    

    #
    # Creación y limpiezade del dataframe df_client
    #
    df_client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']]
    df_client['job'] = df_client['job'].apply(lambda x: x.replace('.', '')).apply(lambda x: x.replace('-', '_'))
    df_client['education'] = df_client['education'].apply(lambda x: x.replace('.', '_')).apply(lambda x: x.replace('unknown', 'pd.NA'))
    df_client['credit_default'] = df_client['credit_default'].apply(lambda x:  1 if x == 'yes' else 0)
    df_client['mortgage'] = df_client['mortgage'].apply(lambda x:  1 if x == 'yes' else 0)
    print(df_client.head(n=30))


    #
    # Creación y limpiezade del dataframe df_campaign
    #
    df_campaign = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome']]
    df_campaign['previous_outcome'] = df_campaign['previous_outcome'].apply(lambda x:  1 if x == 'success' else 0)
    df_campaign['campaign_outcome'] = df_campaign['campaign_outcome'].apply(lambda x:  1 if x == 'yes' else 0)
    df_campaign['last_contact_date'] = pd.to_datetime(df['day'].astype(str) + '-' + df['month'].astype(str) + '-2022', format='%d-%b-%Y')
    df_campaign['last_contact_date'] = df_campaign['last_contact_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    # print(df_campaign.head(n=30))

    #
    # Creación del df_economics y limpieza
    #
    df_economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']]


    #
    # Guardar archivos
    #
    if os.path.exists('files/output'):
        pass
    else:
        os.makedirs('files/output')


    df_client.to_csv('files/output/client.csv', index=False)
    df_campaign.to_csv('files/output/campaign.csv', index=False)
    df_economics.to_csv('files/output/economics.csv', index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()
