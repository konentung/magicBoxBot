from config import Config
dbclient = Config().dbclient

def get_dbclient():
    return dbclient

# 寫入一筆資料
def write_one_data(data):
    dbclient.MongoClient.database.insert_one(data)

# # 寫入多筆資料
# def write_many_datas(data):
#     dbclient.database.insert_many(data)

# 讀取一個collection的所有資料
def read_many_datas():
    data_list = []
    for data in dbclient.MongoClient.database.find():
        data_list.append(data)
    print(data_list)
    return data_list

# 新增使用者資料
def update_user_status(user_id, new_status, new_update_time, display_name=None):
    if dbclient.MongoClient.database.find_one({"user_id": user_id}) is None:
        # 新增使用者
        write_one_data({
            "user_id": user_id,
            "display_name": display_name if display_name else "",
            "status": new_status,
            "update_time": new_update_time
        })
    else:
        # 準備要更新的欄位
        update_data = {
            "status": new_status,
            "update_time": new_update_time
        }
        if display_name:  # 如果有提供 display_name，才會更新
            update_data["display_name"] = display_name

        result = dbclient.MongoClient.database.update_one(
            {"user_id": user_id},  # 查詢條件：根據 user_id
            {"$set": update_data}  # 根據提供的資料更新
        )
        # 檢查是否成功更新
        if result.matched_count > 0:
            print(f"User {user_id} status updated to {new_status}.")
        else:
            print(f"User {user_id} not found.")

def delete_user(user_id):
    # 查詢是否有該筆資料
    result = dbclient.MongoClient.database.find_one({"user_id": user_id})
    if result is None:
        print(f"User {user_id} not found.")
        return
    else:
        print(f"User {user_id} found.")
        dbclient.MongoClient.database.delete_one(
            {"user_id": user_id}
        )

# 紀錄使用者功能
def write_user_func(user_id, func_name, data=None):
    """
    新增或更新使用者功能
    """
    if dbclient.MongoClient.func.find_one({"user_id": user_id}) is None:
        # 新增使用者，func 和 data 一起儲存
        dbclient.MongoClient.func.insert_one({
            "user_id": user_id,
            "func": func_name,
            "data": data  # 若沒有提供 data，將儲存為 None
        })
    else:
        # 更新使用者功能
        update_user_func(user_id, func_name, data)

def update_user_func(user_id, new_func, new_data=None):
    """
    更新使用者功能
    """
    update_data = {"$set": {"func": new_func}}  # 永遠更新 func

    # 如果有提供新的 data，則一併更新
    if new_data is not None:
        update_data["$set"]["data"] = new_data

    result = dbclient.MongoClient.func.update_one(
        {"user_id": user_id},  # 查詢條件：根據 user_id
        update_data  # 更新 func 和 data（如果有）
    )

def get_user_func(user_id):
    """
    取得使用者功能
    """
    user_func = dbclient.MongoClient.func.find_one({
        "user_id": user_id
    })
    return user_func

def delete_user_func(user_id):
    """
    刪除使用者功能
    """
    return dbclient.MongoClient.func.delete_one(
        {"user_id": user_id}
    )

# 紀錄1A2B遊戲解答
def write_user_answer(user_id, answer):
    dbclient.MongoClient.ans.insert_one({
        "user_id": user_id,
        "answer": answer
    })

def delete_user_answer(user_id):
    if dbclient.MongoClient.ans.find_one({"user_id": user_id}) is None:
        return
    else:
        dbclient.MongoClient.ans.delete_one(
            {"user_id": user_id}
        )

def get_user_answer(user_id):
    """
    取得使用者1A2B遊戲解答
    """
    user_answer = dbclient.MongoClient.ans.find_one({
        "user_id": user_id
    })
    return user_answer.get("answer") if user_answer else None

# 紀錄使用者日曆
def write_user_calendar(user_id, datetime, case):
    dbclient.MongoClient.calendar.insert_one({
        "user_id": user_id,
        "datetime": datetime,
        "case": case
    })

def get_user_calendar(user_id):
    """
    取得使用者日曆
    """
    # 查詢資料庫中的紀錄
    user_calendar = dbclient.MongoClient.calendar.find({
        "user_id": user_id
    })
    
    # 如果有資料
    user_records = []
    for record in user_calendar:
        user_records.append(record)

    return user_records