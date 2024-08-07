# Reproduction

trial twisted_trial_editable

Working:
`python -m pip install --config-settings editable_mode=compat -e ./subdir/`

Problem:
`python -m pip install -e ./subdir/`
