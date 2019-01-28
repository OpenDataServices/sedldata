"""deal summary lsoa-region offer improvment

Revision ID: 7ec59cb49f09
Revises: 3d8b428eb9d3
Create Date: 2019-01-25 13:26:30.376649

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7ec59cb49f09'
down_revision = '3d8b428eb9d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sql = '''
    drop index if exists name_key_lookup_table;
    create unique index name_key_lookup_table on lookup_table(lookup_name, lookup_key); 

    CREATE OR REPLACE VIEW public.offer AS
    SELECT offer.value ->> 'id'::text AS offer_id,
       deal.collection,
       deal.id AS deal_table_id,
       deal.deal_id,
       deal.deal ->> 'title'::text AS deal_title,
       deal.deal ->> 'status'::text AS deal_status,
       offer.value AS offer
    FROM deal,
     LATERAL jsonb_array_elements(deal.deal -> 'offers'::text) offer(value)
           where offer.value->'id' is not null;

    drop materialized view collection_summary;
    drop materialized view deal_summary;

    CREATE MATERIALIZED VIEW public.deal_summary
      AS
    SELECT deal.id AS deal_table_id,
        deal.deal_id,
        deal.collection,
        (deal.deal -> 'recipientOrganization'::text) ->> 'name'::text AS recipient_organization_name,
        (deal.deal -> 'recipientOrganization'::text) ->> 'id'::text AS recipient_organization_id,
        (deal.deal -> 'arrangingOrganization'::text) ->> 'name'::text AS arraging_organization_name,
        (deal.deal -> 'arrangingOrganization'::text) ->> 'id'::text AS arraging_organization_id,
        deal.deal ->> 'status'::text AS status,
        deal.deal ->> 'currency'::text AS currency,
        COALESCE(convert_to_numeric(deal.deal ->> 'estimatedValue'::text)::numeric, 0::numeric) AS estimated_value,
        COALESCE(convert_to_numeric(deal.deal ->> 'value'::text)::numeric, 0::numeric) AS value,
        COALESCE(os.offer_count, 0::bigint) AS offer_count,
        COALESCE(os.csu_standard_mark_awarded, 0::bigint) AS csu_standard_mark_awarded,
        COALESCE(os.investment_target, 0::bigint) AS investment_target,
        COALESCE(os.minimum_investment_target, 0::bigint) AS minimum_investment_target,
        COALESCE(os.maximum_investment_target, 0::bigint) AS maximum_investment_target,
        COALESCE(ps.project_estimated_value, 0::bigint) AS project_estimated_value,
        COALESCE(ps.project_raised_value, 0::bigint) AS project_raised_value,
        COALESCE(ps.project_count, 0::bigint) AS project_count,
        COALESCE(ps.asset_purchase_price, 0::numeric) AS asset_purchase_price,
        COALESCE(ps.asset_quantity, 0::numeric) AS asset_quantity,
        COALESCE(ps.asset_count, 0::numeric) AS asset_count,
        COALESCE(ps.asset_value, 0::numeric) AS asset_value,
        COALESCE(gs.grant_count, 0::bigint) AS grant_count,
        COALESCE(gs.is_match_funding, 0::bigint) AS is_match_funding,
        COALESCE(gs.grant_amount_committed, 0::bigint) AS grant_amount_committed,
        COALESCE(gs.grant_amount_disbursed, 0::bigint) AS grant_amount_disbursed,
        COALESCE(gs.grant_amount_requested, 0::bigint) AS grant_amount_requested,
        COALESCE(es.equity_count, 0::bigint) AS equity_count,
        COALESCE(es.equity_value, 0::bigint) AS equity_value,
        COALESCE(es.equity_estimated_value, 0::bigint) AS equity_estimated_value,
        COALESCE(cs.credit_count, 0::bigint) AS credit_count,
        COALESCE(cs.credit_estimated_value, 0::numeric) AS credit_estimated_value,
        COALESCE(cs.credit_value, 0::numeric) AS credit_value,
            loc->>'geoCode' lsoa, 
            lt1.lookup_name imd_type, lt1.data imd_data,
        lt3.data ->> 'nuts1_name' nuts1,
            lt3.data ->> 'nuts2_name' nuts2,
        deal.deal
       FROM deal
         LEFT JOIN offer_summary os ON os.deal_table_id = deal.id
         LEFT JOIN project_summary ps ON ps.deal_table_id = deal.id
         LEFT JOIN grant_summary gs ON gs.deal_table_id = deal.id
         LEFT JOIN equity_summary es ON es.deal_table_id = deal.id
         LEFT JOIN credit_summary cs ON cs.deal_table_id = deal.id
             left join jsonb_array_elements(deal->'recipientOrganization'->'location') as loc on loc->>'geoCodeType' = 'lsoa' 
             LEFT JOIN lookup_table lt1 on lt1.lookup_name in ('imd_england', 'imd_scotland', 'imd_wales') and lt1.lookup_key = loc->>'geoCode'
             LEFT JOIN lookup_table lt2 on lt2.lookup_name = 'nuts3_post' and lt2.lookup_key = upper(replace(replace(trim(deal->'recipientOrganization'->>'postalCode'), ' ',''), E'\n', ''))
             LEFT JOIN lookup_table lt3 on lt3.lookup_name = 'nuts2_codes' and lt3.lookup_key = lt2.data ->> 'NUTS_2';


                                                                                                                                                                                                             
    CREATE MATERIALIZED VIEW public.collection_summary
    AS
     SELECT deal_summary.collection,
        count(*) AS deal_count,
        sum(deal_summary.estimated_value) AS estimated_value,
        sum(deal_summary.value) AS value,
        sum(deal_summary.offer_count) AS offer_count,
        sum(deal_summary.csu_standard_mark_awarded) AS csu_standard_mark_awarded,
        sum(deal_summary.investment_target) AS investment_target,
        sum(deal_summary.minimum_investment_target) AS minimum_investment_target,
        sum(deal_summary.maximum_investment_target) AS maximum_investment_target,
        sum(deal_summary.project_estimated_value) AS project_estimated_value,
        sum(deal_summary.project_raised_value) AS project_raised_value,
        sum(deal_summary.project_count) AS project_count,
        sum(deal_summary.asset_purchase_price) AS asset_purchase_price,
        sum(deal_summary.asset_quantity) AS asset_quantity,
        sum(deal_summary.asset_count) AS asset_count,
        sum(deal_summary.asset_value) AS asset_value,
        sum(deal_summary.grant_count) AS grant_count,
        sum(deal_summary.is_match_funding) AS is_match_funding,
        sum(deal_summary.grant_amount_committed) AS grant_amount_committed,
        sum(deal_summary.grant_amount_disbursed) AS grant_amount_disbursed,
        sum(deal_summary.grant_amount_requested) AS grant_amount_requested,
        sum(deal_summary.equity_count) AS equity_count,
        sum(deal_summary.equity_value) AS equity_value,
        sum(deal_summary.equity_estimated_value) AS equity_estimated_value,
        sum(deal_summary.credit_count) AS credit_count,
        sum(deal_summary.credit_estimated_value) AS credit_estimated_value,
        sum(deal_summary.credit_value) AS credit_value
       FROM deal_summary
      GROUP BY deal_summary.collection;
    '''
    op.execute(sql)
    
    # ### end Alembic commands ###


def downgrade():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
