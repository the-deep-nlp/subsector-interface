import streamlit as st
import sqlalchemy as sa
import pandas as pd
import db_orm
import app
import constants
import ast
from guidelines import guidelines
from time import sleep
from datetime import date

st.set_page_config(layout="wide")

class AddEntryTag():
    def __init__(self):
        pass

    def _get_list_of_users(self):
        df = pd.read_sql_table('Users', app.engine)
        return df['name'].to_list()

    def create_page(self):
        # Load Guidlines in the sidebar
        guidelines()

        selected_user = st.selectbox(
            "Select the Tagger",
            self._get_list_of_users()
        )

        selected_user_id = app.session.query(db_orm.Users).filter(db_orm.Users.name==selected_user).first().id

        total_items_count = app.session.query(db_orm.Sectors).filter(
            db_orm.Sectors.assigned_to==selected_user_id
        ).count()
        pending_items_count = app.session.query(db_orm.Sectors).filter(
            db_orm.Sectors.assigned_to==selected_user_id,
            db_orm.Sectors.complete==False
        ).count()

        if total_items_count:
            st.write(f"Progress of {selected_user}")
            percent = int((total_items_count - pending_items_count)/(total_items_count)* 100)
            st.progress(percent)
        else:
            st.warning("No task assigned")

        sa_table = sa.Table("Sectors", sa.MetaData(), autoload_with=app.engine)
        sa_query = sa.select([sa_table]).where(sa_table.c.assigned_to==selected_user_id,sa_table.c.complete==False)
        df = pd.read_sql_query(sa_query, app.engine)

        # to fix the skipped rows
        #df = df.drop(labels=[0], axis=0).reset_index()

        try:
            sector_default = ast.literal_eval(df.iloc[0].sector)
        except Exception as e:
            sector_default = None
        
        try:
            subsector_default = ast.literal_eval(df.iloc[0].subsector)
        except Exception as e:
            subsector_default = None
        
        try:
            subsubsector_default = ast.literal_eval(df.iloc[0].subsubsector)
        except Exception as e:
            subsubsector_default = None
        
        try:
            subsubsubsector_default = ast.literal_eval(df.iloc[0].subsubsubsector)
        except Exception as e:
            subsubsubsector_default = None
        
        try:
            subsubsubsubsector_default = ast.literal_eval(df.iloc[0].subsubsubsubsector)
        except Exception as e:
            subsubsubsubsector_default = None

        if len(df):
            self.id = st.text_input("Entry Id", value=df.iloc[0].entry_id, disabled=True)
            self.excerpt = st.text_area("Excerpt", value=df.iloc[0].excerpt, disabled=True)
            
            # Sector
            self.sector = st.multiselect(
                "Sector",
                options=constants.data_df["sector"].unique().tolist(),
                default=sector_default
            )

            df_join_1 = constants.data_df[constants.data_df["sector"].isin(self.sector)][["sector", "subsector"]]
            df_join_1["processed_subsector"] = df_join_1["sector"].astype(str) + "->" + df_join_1["subsector"].astype(str) #join_df[["sector", "subsector"]].apply("-".join, axis=1)

            # Sub sector
            self.sub_sector = st.multiselect(
                "SubSector",
                options=df_join_1["processed_subsector"].unique().tolist(), #constants.data_df[constants.data_df["sector"].isin(self.sector)]["subsector"].unique().tolist(),
                default=subsector_default
            )

            sub_sector_lst = list(map(lambda x: x.split("->")[-1], self.sub_sector))
            df_join_2 = constants.data_df[constants.data_df["subsector"].isin(sub_sector_lst)][["sector", "subsector", "subsubsector"]]
            df_join_2["processed_sub_sub_sector"] = df_join_2["sector"].astype(str) + "->" + df_join_2["subsector"].astype(str) + "->" + df_join_2["subsubsector"].astype(str)

            # Sub sub sector
            self.sub_sub_sector = st.multiselect(
                "SubSubSector",
                options=df_join_2["processed_sub_sub_sector"].unique().tolist(),  #constants.data_df[constants.data_df["subsector"].isin(self.subsector)]["subsubsector"].unique().tolist(),
                default=subsubsector_default
            )

            # Sub sub sub sector
            sub_sub_sector_lst = list(map(lambda x: x.split("->")[-1], self.sub_sub_sector))
            df_join_3 = constants.data_df[constants.data_df["subsubsector"].isin(sub_sub_sector_lst)][["sector", "subsector", "subsubsector", "subsubsubsector"]]
            df_join_3["processed_sub_sub_sub_sector"] = df_join_3["sector"].astype(str) + "->" + df_join_3["subsector"].astype(str) + "->" + df_join_3["subsubsector"].astype(str) + "->" + df_join_3["subsubsubsector"].astype(str)

            self.sub_sub_sub_sector = st.multiselect(
                "SubSubSubSector",
                options=df_join_3["processed_sub_sub_sub_sector"].unique().tolist(),
                default=subsubsubsector_default
            )

            # Sub sub sub sub sector
            sub_sub_sub_sector_lst = list(map(lambda x: x.split("->")[-1], self.sub_sub_sub_sector))
            df_join_4 = constants.data_df[constants.data_df["subsubsubsector"].isin(sub_sub_sub_sector_lst)][["sector", "subsector", "subsubsector", "subsubsubsector", "subsubsubsubsector"]]
            df_join_4["processed_sub_sub_sub_sub_sector"] = df_join_4["sector"].astype(str) + "->" + df_join_4["subsector"].astype(str) + "->" + df_join_4["subsubsector"].astype(str) + "->" + df_join_4["subsubsubsector"].astype(str) + "->" + df_join_4["subsubsubsubsector"].astype(str)

            self.sub_sub_sub_sub_sector = st.multiselect(
                "SubSubSubSubSector",
                options=df_join_4["processed_sub_sub_sub_sub_sector"].unique().tolist(),
                default=subsubsubsubsector_default
            )

            self.comment = st.text_area("Comment", value=df.iloc[0].comment)

            self.submit_btn = st.button(label="Submit")

            if self.submit_btn:
                try:
                    app.session.query(db_orm.Sectors).filter(
                        db_orm.Sectors.entry_id==int(df.iloc[0].entry_id)
                    ).update(
                        {
                            "sector": str(self.sector),
                            "subsector": str(self.sub_sector),
                            "subsubsector": str(self.sub_sub_sector),
                            "subsubsubsector": str(self.sub_sub_sub_sector),
                            "subsubsubsubsector": str(self.sub_sub_sub_sub_sector),
                            "last_tagged_date": date.today(),
                            "comment": str(self.comment),
                            "complete": True
                        }
                    )
                    app.session.commit()
                    st.info("Database is updated.")
                except Exception as e:
                    st.error(f"Failed to update database. {e}")
                sleep(1)
                st.experimental_rerun()
        else:
            st.info("No task found or All complete")


add_entry_tag = AddEntryTag()
add_entry_tag.create_page()