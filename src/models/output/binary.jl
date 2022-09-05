"""
Output module
Pengfei Cheng

Create the DataFrame for the binary variables.
"""

function gen_binary_df(m)

    binary_vars = ["y", "z0", "z"]

    # add columns
    l0 = []
    for v in binary_vars
        local l = [v => Float64[]]
        # extend array l0
        l0 = vcat(l0, l)
    end

    df_binary = DataFrame(l0)
    # add the values to the DataFrame

    for i in set_hour
        local l0 = []
        for v in binary_vars
            s = Symbol(v)
            local l = [value(m[s][i])]
            l0 = vcat(l0, l)
        end
        push!(df_binary, l0)
    end

    return df_binary
end