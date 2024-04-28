import requests as rq
import pandas as pd
from datetime import datetime, timedelta
from IPython.display import clear_output

class LentaRuParser:
    def __init__(self):
        pass

    def _get_url(self, param_dict: dict) -> str:
        """
        Returns the URL for requesting a JSON table with articles.
        """
        hasType = int(param_dict['type']) != 0
        hasBloc = int(param_dict['bloc']) != 0

        url = f'https://lenta.ru/search/v2/process?' \
            + f'from={param_dict["from"]}&' \
            + f'size={param_dict["size"]}&' \
            + f'sort={param_dict["sort"]}&' \
            + f'title_only={param_dict["title_only"]}&' \
            + f'domain={param_dict["domain"]}&' \
            + f'modified%2Cformat=yyyy-MM-dd&' \
            + f'type={param_dict["type"] * hasType}&' \
            + f'bloc={param_dict["bloc"] * hasBloc}&' \
            + f'modified%2Cfrom={param_dict["dateFrom"]}&' \
            + f'modified%2Cto={param_dict["dateTo"]}&' \
            + f'query={param_dict["query"]}'

        return url

    def _get_search_table(self, param_dict: dict) -> pd.DataFrame:
        """
        Returns a pd.DataFrame with the list of articles.
        """
        url = self._get_url(param_dict)
        r = rq.get(url)
        search_table = pd.DataFrame(r.json()['matches'])

        return search_table

    def get_articles(self, param_dict, time_step=37, save_every=5, save_excel=True) -> pd.DataFrame:
        """
        Function to download articles at intervals of every time_step days.
        Saves the table every save_every * time_step days.
        """
        param_copy = param_dict.copy()
        time_step = timedelta(days=time_step)
        dateFrom = datetime.strptime(param_copy['dateFrom'], '%Y-%m-%d')
        dateTo = datetime.strptime(param_copy['dateTo'], '%Y-%m-%d')
        if dateFrom > dateTo:
            raise ValueError('dateFrom should be less than dateTo')

        out = pd.DataFrame()
        save_counter = 0

        while dateFrom <= dateTo:
            param_copy['dateTo'] = (dateFrom + time_step).strftime('%Y-%m-%d')
            if dateFrom + time_step > dateTo:
                param_copy['dateTo'] = dateTo.strftime('%Y-%m-%d')
            print('Parsing articles from ' + param_copy['dateFrom'] + ' to ' + param_copy['dateTo'])
            out = out.append(self._get_search_table(param_copy), ignore_index=True)
            dateFrom += time_step + timedelta(days=1)
            param_copy['dateFrom'] = dateFrom.strftime('%Y-%m-%d')
            save_counter += 1
            if save_counter == save_every:
                clear_output(wait=True)
                out.to_excel("/tmp/checkpoint_table.xlsx")
                print('Checkpoint saved!')
                save_counter = 0

        if save_excel:
            out.to_excel(f"lenta_{param_dict['dateFrom']}_{param_dict['dateTo']}.xlsx")
        print('Finish')

        return out

# Example of parser invocation
query = ''
offset = 0
size = 1000
sort = "3"
title_only = "0"
domain = "1"
material = "0"
bloc = "0"
dateFrom = '2023-01-01'
dateTo = "2023-12-30"

param_dict = {
    'query': query,
    'from': str(offset),
    'size': str(size),
    'dateFrom': dateFrom,
    'dateTo': dateTo,
    'sort': sort,
    'title_only': title_only,
    'type': material,
    'bloc': bloc,
    'domain': domain
}

print("param_dict:", param_dict)

parser = LentaRuParser()

tbl = parser.get_articles(param_dict=param_dict, time_step=37, save_every=5, save_excel=True)
print(len(tbl.index))
tbl.head()
