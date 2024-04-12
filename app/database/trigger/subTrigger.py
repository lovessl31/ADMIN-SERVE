def cst(cursor):
    # 입력 동작
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS sync_to_main_db_trigger AFTER INSERT ON sub_table
        BEGIN
            -- 메인 데이터베이스로 데이터를 동기화하는 쿼리
            INSERT INTO main_table (column1, column2, ...)
            VALUES (NEW.column1, NEW.column2, ...);
        END;
    ''')

    # 삭제 동작
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS sync_delete_to_main_db_trigger AFTER DELETE ON sub_table
        BEGIN
            -- 메인 데이터베이스에서 해당 데이터 삭제
            DELETE FROM main_table WHERE id = OLD.id;
        END;
    ''')