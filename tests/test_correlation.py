from scripts.data_gen import generate_synthetic_data

# TODO: turn into test function
synth_data = generate_synthetic_data(exam="oxidative", n_members=10)

corr_synth = synth_data.corr()
print("corr_synth")
print(corr_synth)
print(type(synth_data.corr()))

with open("resources/biomarkers.json", 'r') as f:
    corr_matrix = pd.DataFrame(json.load(f)["oxidative"]["correlationMatrix"])

print("-----", "corr_matrix")
print(corr_matrix)
diff = corr_matrix == corr_synth
