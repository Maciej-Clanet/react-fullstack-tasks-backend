from bson import ObjectId
from fastapi import APIRouter, HTTPException
from db import db, to_object_id, serialize_doc

from tasks.example.models import AddPerson, AddPersonResponse, UpdatePerson

# Need to create a router to make these paths visible to the app, import the router in main.py
example_router = APIRouter()

# Any collections you will need to interact with.
# You can use multiple collections as well, just have multiple variables
example_collection = db["example_collection"]


# ADD A PERSON
@example_router.post("/people", response_model=AddPersonResponse)
def example_add(person: AddPerson):

    # This will copy all the person values into a dictionary, keeping the same keys and values
    person_dict = person.model_dump()

    # keeping the result is optional, but can be used to get ID of the inserted data
    result = example_collection.insert_one(person_dict)

    # Every mongo db document has an ID
    # This has an data type of object id, we will need to convert it to string for most use cases
    inserted_id = result.inserted_id

    return AddPersonResponse(message="New person added", id=str(inserted_id))


# GET ALL PEOPLE
@example_router.get("/people")
def get_all():
    # In mongo, search result return something called a "cursor"
    cursor = example_collection.find()

    # we can loop over it to extract the value
    people = []
    for doc in cursor:
        # convert to json friendly types
        serialized = serialize_doc(doc)
        people.append(serialized)

    # alternative ways to do this in less code
    """
        #1 - This is syntax for map in python, functions similar to map in JavaScript
        people = list(map(serialize_doc, cursor))
    
        #2 - Some cursed python syntax, also basically a map
        people = [serialize_doc(doc) for doc in cursor]
    """
    return {"count": len(people), "items": people}


# GET ALL BY ROLE, OPTION 1, use path parameters
@example_router.get("/people/role/{role}")
def get_people_by_role_path(role: str):
    cursor = example_collection.find({"role": role})
    people = [serialize_doc(doc) for doc in cursor]
    return {"role": role, "count": len(people), "items": people}


# GET ALL BY ROLE, OPTION 2, use query parameters
@example_router.get("/people/role")
def get_people_by_role_query(role: str):
    cursor = example_collection.find({"role": role})
    people = [serialize_doc(doc) for doc in cursor]

    return {"role": role, "count": len(people), "items": people}


# GET ALL WITH NO ROLE
@example_router.get("/people/norole")
def get_all_with_no_role():
    cursor = example_collection.find({"role": None})
    people = [serialize_doc(doc) for doc in cursor]
    return {"role": None, "count": len(people), "items": people}


# DELETE A PERSON BY ID
# for delete endpoints, its considered good practice to get the data from the url itself
@example_router.delete("/people/{id}")
def example_delete(id: str):

    # convert string version in object mongo can understand
    # this function is imported from our db file, had to be manually made there
    object_id = to_object_id(id)

    result = example_collection.delete_one({"_id": object_id})
    print(result)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Person not found")

    return {"message": "Person Deleted", "deleted_count": result.deleted_count}


# UPDATE PERSON BY ID
@example_router.patch("/people/{id}")
def update_person(id: str, updates: UpdatePerson):
    object_id = to_object_id(id)

    # exclude_unset will make it ignore null values
    update_data = updates.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    result = example_collection.update_one(
        {"_id": object_id}, {"$set": update_data}
    )  # set will only change the provided fields

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Person not found")

    updated_doc = example_collection.find_one({"_id": object_id})
    return {
        "message": "Person updated",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "item": serialize_doc(updated_doc),
    }
