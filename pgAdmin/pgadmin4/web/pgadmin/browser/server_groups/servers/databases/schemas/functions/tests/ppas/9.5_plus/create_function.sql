-- FUNCTION: public.Function1_$%{}[]()&*^!@"'`\/#(character varying)

-- DROP FUNCTION public."Function1_$%{}[]()&*^!@""'`\/#"(character varying);

CREATE OR REPLACE FUNCTION public."Function1_$%{}[]()&*^!@""'`\/#"(
	param character varying DEFAULT '1'::character varying)
RETURNS character varying
    LANGUAGE 'plpgsql'
    VOLATILE LEAKPROOF STRICT SECURITY DEFINER WINDOW
    COST 100
    SET enable_sort='true'
AS $BODY$
begin
select '1';
end
$BODY$;

ALTER FUNCTION public."Function1_$%{}[]()&*^!@""'`\/#"(character varying)
    OWNER TO enterprisedb;
