function rename_df_col(df)

    # preprocess column name
    col = Symbol[]

    for i in string.(names(df))
        i = replace(strip(i), " " => "_", "-" => "", "/" => "", "(" => "", ")" => "", "%" => "", "," => "", "*" => "", "+" => "")

        push!(col, Symbol(i))
    end

    rename!(df, col)

    df
end

function lin_reg_df(df, var_pairs)

    # create formula array
    formulae = FormulaTerm[]

    # build formula
    for (y, x) in var_pairs

        # the macro @formula is not used here, as y, x are symbols
        # formula_ST = @formula(eval(y) ~ eval(x))
        _formula = Term(y) ~ Term(x)
        push!(formulae, _formula)
    end

    # create coefficient df
    coef_df = DataFrame(
        y = String[], 
        x = String[], 
        b = Float64[], 
        a = Float64[])


    for _formula in formulae

        # linear regression
        linReg = lm(_formula, df)

        # y (name)
        y = string(terms(_formula)[1])

        # x (name)
        x = string(terms(_formula)[1])

        # intercept
        b = coef(linReg)[1]

        # slope
        a = coef(linReg)[2]

        # output results
        push!(coef_df, (y, x, b, a))

        # println(linReg)
        # println(deviance(linReg))
        # println(coef(linReg))
        end
    
    coef_df
end