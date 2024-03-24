import numpy as np


def get_pval_text(p_val):
    """Report p-value in latex."""
    if p_val < 0.001:
        ptext = "p < 0.001"
    else:
        ptext = f"p = {p_val:.3f}"
    return ptext


def get_pval_string(p_val):
    """Get significance stars for p-value."""
    if p_val > 0.05:
        return ""
    elif p_val < 0.001:
        return "^{***}"
    elif p_val < 0.01:
        return "^{**}"
    else:
        return "^{*}"


def get_mann_whitney_text(comparison, pval : float = None, table: bool=False, alternative:bool=False):
    """Get Mann-Whitney test report."""
    pval_prefix = "\\text{adj.} "
    if pval is None:
        pval = comparison['p-val'].values[0]
        pval_prefix = ""
    pval_text = pval_prefix + get_pval_text(pval)

    alternative_text = ""
    if alternative:
        alternative_text = f", $\\text{{{comparison['alternative'].values[0]}}}$"
        if table:
            alternative_text = " & \\text{{{comparison['alternative'].values[0]}}} "

    if table:
        return f"{comparison['U-val'].values[0]:.2f} & {pval:.3f} & {comparison['RBC'].values[0]:.2f} \\\ "

    return (
        f"Mann-Whitney $U={comparison['U-val'].values[0]:.2f}$, "
        f"$\\text{{RBC}} = {comparison['RBC'].values[0]:.2f}$, "
        f"${pval_text}${alternative_text}"
    )


def get_wilcoxon_text(comparison, pval=None):
    """Get Wilcoxon test report."""
    if pval is None:
        pval_text = get_pval_text(comparison['p-val'].values[0])
    else:
        pval_text = "\\text{adj.} " + get_pval_text(pval)

    return (
        f"$W = {comparison['W-val'].values[0]:.2f}$, "
        f"$\\text{{RBC}} = {comparison['RBC'].values[0]:.2f}$,"
        f" ${pval_text}$, "
        f"{comparison['alternative'].values[0]}"
    )


def get_friedman_test_text(comparison, pval=None):
    """Get Friedman test report."""
    if pval is None:
        pval_text = get_pval_text(comparison['p-unc'].values[0])
    else:
        pval_text = "$\\text{adj.}" + get_pval_text(pval)

    if hasattr(comparison, "Q"):
        return (
            f"$\\chi^2({comparison.ddof1[0]}) = "
            f"{comparison.Q[0]:.3f}$, "
            f"${get_pval_text(comparison['p-unc'].values[0])}$"
        )
    if hasattr(comparison, "F"):
        return (
            f"$F({comparison.ddof1[0]:.2f}, "
            f"{comparison.ddof2[0]:.2f}) = "
            f"{comparison.F[0]:.3f}$, "
            f"${pval_text}$"
        )


def get_kruskal_wallis_text(comparison, pval=None):
    """Get Kruskal-Wallis test report."""
    if pval is None:
        pval_text = get_pval_text(comparison['p-unc'].values[0])
    else:
        pval_text = "$\\text{adj.}" + get_pval_text(pval)

    return (
        f"Kruskal-Wallis $H({comparison['ddof1'].values[0]})"
        f" = {comparison['H'].values[0]:.2f}$, "
        f"${pval_text}$"
    )


def get_correlation_text(correlation, table=False, pval=None):
    """Get correlation test report."""
    if pval is None:
        pval_text = get_pval_text(correlation['p-val'].values[0])
    else:
        pval_text = "\\text{adj.} " + get_pval_text(pval)

    if np.any(np.isnan(correlation["CI95%"][0])):
        return "Potentially no variance of one parameter..."

    if table is True:
        sep = " & "
        ci_sep = ""
    else:
        sep = ", "
        ci_sep = "95\%\ C.\ I.\: "

    if "pearson" in correlation.index.values:
        return (
            f"$r({correlation['n'].values[0]}) = {correlation['r'].values[0]:.2f}${sep}"
            f"${pval_text}${sep}{ci_sep}"
            f"$[{correlation['CI95%'][0][0]:.2f}, {correlation['CI95%'][0][1]:.2f}]$"
        )
    elif "spearman" in correlation.index.values:
        return (
            f"Spearman's $\\rho({correlation['n'].values[0]}) ="
            f" {correlation['r'].values[0]:.2f}${sep}"
            f"${pval_text}${sep}{ci_sep}"
            f"$[{correlation['CI95%'][0][0]:.2f}, {correlation['CI95%'][0][1]:.2f}]$"
        )
    else:
        raise NotImplementedError


def get_ttest_text(comparison, pval=None):
    """Get t-test report."""
    if pval is None:
        pval_text = get_pval_text(comparison['p-val'].values[0])
    else:
        pval_text = "\\text{adj.} " + get_pval_text(pval)

    if isinstance(comparison["dof"].values[0], int) or isinstance(
        comparison["dof"].values[0], np.int64
    ):
        dof = comparison["dof"].values[0]
    else:
        dof = f"{comparison['dof'].values[0]:.2f}"
    return (
        f"$t({dof}) = {comparison['T'].values[0]:.2f}$,"
        f" ${pval_text}$"
    )


def get_regression_text(regression_res, pval=None):
    """Get regression test report."""
    if pval is None:
        pval_text = get_pval_text(regression_res.f_pvalue)
    else:
        pval_text = "\\text{adj.} " + get_pval_text(pval)

    return (
        f"adj. $R^2={regression_res.rsquared_adj:.2f}$, "
        f"$F({regression_res.df_model:.0f}, {regression_res.df_resid:.0f}) = "
        f"{regression_res.fvalue:.2f}$, ${pval_text}$"
    )


def get_parameter_coefficient(regression_res, param, pval=None):
    """Get regression parameter coefficient report."""
    if pval is None:
        pval_text = get_pval_text(regression_res.pvalues[param])
    else:
        pval_text = "\\text{adj.} " + get_pval_text(pval)

    return (
        f"$t({regression_res.df_resid:.0f}) = "
        f"{regression_res.tvalues[param]:.2f}$, "
        f"${pval_text}$, "
        f"$\\beta = {regression_res.params[param]:.2f}$"
    )