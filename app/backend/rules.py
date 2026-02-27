def detect_errors(tree):

    errors = []
    warnings = []

    # Rule 1: Missing TryCatch
    if not tree.xpath("//*[local-name()='TryCatch']"):
        errors.append("No Try Catch found")

    # Rule 2: Hard Delay
    if tree.xpath("//*[local-name()='Delay']"):
        warnings.append("Hard Delay detected – use Retry Scope")

    # Rule 3: No logging
    if not tree.xpath("//*[contains(@DisplayName,'Log')]"):
        warnings.append("No logging activity")

    # Rule 4: Excel inside loop
    loops = tree.xpath("//*[local-name()='ForEach']")
    excels = tree.xpath("//*[contains(@DisplayName,'Excel')]")

    if loops and excels:
        errors.append("Excel used inside loop – performance issue")

    return errors, warnings