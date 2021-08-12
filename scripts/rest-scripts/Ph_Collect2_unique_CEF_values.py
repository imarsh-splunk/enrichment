import json

filtered_artifacts_data_1 = [
    [
        "45.127.98.1",
        243943
    ],
    [
        "45.127.98.1",
        243944
    ]
]

print(filtered_artifacts_data_1)



e1 = filtered_artifacts_data_1[0]

print(e1)


unique_artifacts_data = list(map(list, set(map(lambda i: tuple(i), filtered_artifacts_data_1))))


print(type(unique_artifacts_data))
print(unique_artifacts_data)
