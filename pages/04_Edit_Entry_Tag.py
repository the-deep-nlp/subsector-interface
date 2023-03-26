import streamlit as st
import sqlalchemy as sa
import pandas as pd
import db_orm
import app
import constants
import ast
from datetime import date
from guidelines import guidelines
from time import sleep
from datetime import date

st.set_page_config(layout="wide")

class EditEntryTag():
    def __init__(self):
        try:
            app.engine.connect()
            self.db_status = True
        except Exception:
            self.db_status = False
            st.subheader("Database connection failed.")

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

        selected_entry_id = st.number_input("Entry ID", min_value=1)

        sa_table = sa.Table("Sectors", sa.MetaData(), autoload_with=app.engine)
        sa_query = sa.select([sa_table]).where(
            sa_table.c.assigned_to==selected_user_id,
            sa_table.c.entry_id==selected_entry_id)
        df = pd.read_sql_query(sa_query, app.engine)

        # to fix the skipped rows
        #df = df.drop(labels=[0], axis=0).reset_index()

        try:
            sector_default = ast.literal_eval(df.iloc[0].sector)
        except Exception as e:
            sector_default = []
        
        try:
            subsector_default = ast.literal_eval(df.iloc[0].subsector)
        except Exception as e:
            subsector_default = []
        
        try:
            subsubsector_default = ast.literal_eval(df.iloc[0].subsubsector)
        except Exception as e:
            subsubsector_default = []
        
        try:
            subsubsubsector_default = ast.literal_eval(df.iloc[0].subsubsubsector)
        except Exception as e:
            subsubsubsector_default = []
        
        try:
            subsubsubsubsector_default = ast.literal_eval(df.iloc[0].subsubsubsubsector)
        except Exception as e:
            subsubsubsubsector_default = []
        
        if len(df):
            self.id = st.text_input("Entry Id", value=df.iloc[0].entry_id, disabled=True)
            self.excerpt = st.text_area("Excerpt", value=df.iloc[0].excerpt, disabled=True)

            # Sector
            def sector_session_state():
                st.session_state["sector"] = st.session_state["key_sector"]
            
            sector_1 = constants.data_df["sector"].unique().tolist()
            st.session_state["sector"] = list(set(st.session_state.get("sector", sector_default)).intersection(set(sector_1)))

            self.sector = st.multiselect(
                "Sector",
                options=sector_1,
                default=st.session_state.get("sector", []),
                on_change=sector_session_state,
                key="key_sector"
            )

            df_join_1 = constants.data_df[constants.data_df["sector"].isin(self.sector)][["sector", "subsector"]]
            df_join_1["processed_subsector"] = df_join_1["sector"].astype(str) + "->" + df_join_1["subsector"].astype(str) #join_df[["sector", "subsector"]].apply("-".join, axis=1)

            subsector_1 = df_join_1["processed_subsector"].unique().tolist()
            st.session_state["sub_sector"] = list(set(st.session_state.get("sub_sector", subsector_default)).intersection(set(subsector_1)))

            def sub_sector_session_state():
                st.session_state["sub_sector"] = st.session_state["key_sub_sector"]

            # Sub sector
            self.sub_sector = st.multiselect(
                "SubSector",
                options=subsector_1, #df_join_1["processed_subsector"].unique().tolist(), #constants.data_df[constants.data_df["sector"].isin(self.sector)]["subsector"].unique().tolist(),
                default=st.session_state.get("sub_sector", []),
                on_change=sub_sector_session_state,
                key="key_sub_sector"
            )

            sub_sector_lst = list(map(lambda x: x.split("->")[-1], self.sub_sector))
            df_join_2 = constants.data_df[constants.data_df["subsector"].isin(sub_sector_lst)][["sector", "subsector", "subsubsector"]]
            df_join_2["processed_sub_sub_sector"] = df_join_2["sector"].astype(str) + "->" + df_join_2["subsector"].astype(str) + "->" + df_join_2["subsubsector"].astype(str)

            subsubsector_1 = df_join_2["processed_sub_sub_sector"].unique().tolist() #list(set(df_join_2["processed_sub_sub_sector"].unique().tolist()).difference(set(st.session_state.get("sub_sub_sector", []))))
            st.session_state["sub_sub_sector"] = list(set(st.session_state.get("sub_sub_sector", subsubsector_default)).intersection(set(subsubsector_1)))

            if not subsubsector_1:
                st.session_state["sub_sub_sector"] = []

            def manage_sub_sub_sector():
                st.session_state["sub_sub_sector"] = st.session_state["key_sub_sub_sector"]

            # Sub sub sector
            self.sub_sub_sector = st.multiselect(
                "SubSubSector",
                options=subsubsector_1, #df_join_2["processed_sub_sub_sector"].unique().tolist(),  #constants.data_df[constants.data_df["subsector"].isin(self.subsector)]["subsubsector"].unique().tolist(),
                default=st.session_state.get("sub_sub_sector", []),
                on_change=manage_sub_sub_sector,
                key="key_sub_sub_sector"

            )

            st.session_state["sub_sub_sector"] = self.sub_sub_sector or []

            # Sub sub sub sector
            sub_sub_sector_lst = list(map(lambda x: x.split("->")[-1], self.sub_sub_sector))
            df_join_3 = constants.data_df[constants.data_df["subsubsector"].isin(sub_sub_sector_lst)][["sector", "subsector", "subsubsector", "subsubsubsector"]]
            df_join_3["processed_sub_sub_sub_sector"] = df_join_3["sector"].astype(str) + "->" + df_join_3["subsector"].astype(str) + "->" + df_join_3["subsubsector"].astype(str) + "->" + df_join_3["subsubsubsector"].astype(str)

            subsubsubsector_1 = df_join_3["processed_sub_sub_sub_sector"].unique().tolist()
            st.session_state["sub_sub_sub_sector"] = list(set(st.session_state.get("sub_sub_sub_sector", subsubsubsector_default)).intersection(set(subsubsubsector_1)))

            def manage_sub_sub_sub_sector():
                st.session_state["sub_sub_sub_sector"] = st.session_state["key_sub_sub_sub_sector"]

            self.sub_sub_sub_sector = st.multiselect(
                "SubSubSubSector",
                options=subsubsubsector_1,
                default=st.session_state.get("sub_sub_sub_sector", []), #subsubsubsector_default,
                on_change=manage_sub_sub_sub_sector,
                key="key_sub_sub_sub_sector"
            )

            st.session_state["sub_sub_sub_sector"] = self.sub_sub_sub_sector or []

            # Sub sub sub sub sector
            sub_sub_sub_sector_lst = list(map(lambda x: x.split("->")[-1], self.sub_sub_sub_sector))
            df_join_4 = constants.data_df[constants.data_df["subsubsubsector"].isin(sub_sub_sub_sector_lst)][["sector", "subsector", "subsubsector", "subsubsubsector", "subsubsubsubsector"]]
            df_join_4["processed_sub_sub_sub_sub_sector"] = df_join_4["sector"].astype(str) + "->" + df_join_4["subsector"].astype(str) + "->" + df_join_4["subsubsector"].astype(str) + "->" + df_join_4["subsubsubsector"].astype(str) + "->" + df_join_4["subsubsubsubsector"].astype(str)

            subsubsubsubsector_1 = df_join_4["processed_sub_sub_sub_sub_sector"].unique().tolist()
            st.session_state["sub_sub_sub_sub_sector"] = list(set(st.session_state.get("sub_sub_sub_sub_sector", subsubsubsubsector_default)).intersection(set(subsubsubsubsector_1)))

            def manage_sub_sub_sub_sub_sector():
                st.session_state["sub_sub_sub_sub_sector"] = st.session_state["key_sub_sub_sub_sub_sector"]

            self.sub_sub_sub_sub_sector = st.multiselect(
                "SubSubSubSubSector",
                options=subsubsubsubsector_1,
                default=st.session_state.get("sub_sub_sub_sub_sector", []), #subsubsubsubsector_default,
                on_change=manage_sub_sub_sub_sub_sector,
                key="key_sub_sub_sub_sub_sector"
            )

            st.session_state["sub_sub_sub_sub_sector"] = self.sub_sub_sub_sub_sector or []

            self.comment = st.text_area("Comment", value=df.iloc[0].comment)

            self.supervisor_comment = st.text_area(
                "Supervisor Comment",
                value=df.iloc[0].supervisor_comment,
                disabled=True
            )

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
                            "complete": True,
                            "reviewed": False,
                            "validated": False
                        }
                    )
                    app.session.commit()
                    st.info("Database is updated.")
                except Exception as e:
                    st.error(f"Failed to update database. {e}")
                finally:
                    st.session_state["sector"] = []
                    st.session_state["sub_sector"] = []
                    st.session_state["sub_sub_sector"] = []
                    st.session_state["sub_sub_sub_sector"] = []
                    st.session_state["sub_sub_sub_sub_sector"] = []
                sleep(1)
                st.experimental_rerun()
        else:
            st.info("No record found.")

add_entry_tag = EditEntryTag()
if add_entry_tag.db_status:
    add_entry_tag.create_page()