# Project Social Contract

*Jurisdiction-Agnostic Payroll Calculation Engine*

## Project Purpose

This project exists to provide a generic, predictable, and extensible payroll calculation engine, jurisdiction-agnostic,
that allows organizations and implementers to define their own payroll rules without needing to modify the engine's source code.

**The project does not intend to:**

 - Impose legal interpretations.
 - Replace professional knowledge.
 - Guarantee regulatory compliance.

**What the project promises to its users**

The project promises, *in good faith*, that the engine:

 - Will execute calculations in a predictable and reproducible manner.
 - Will remain jurisdiction-agnostic.
 - Will not incorporate hardcoded legal rules.
 - Will maintain a strict separation between:
     * Calculation engine.
     * Rule configuration.
     * Payroll orchestration.
 - Will allow any legal or policy change to be made through configuration, not through code changes.
 - Will provide sufficient technical traceability to audit calculations.

## Declared Functional Scope

The project explicitly declares that the engine, by default, only does the following:

 - Calculates the employee's base salary according to the period defined in the payroll.
 - Applies salary advance installments when they exist, consuming them from an external module.

Every other payroll concept:

 - Earnings
 - Deductions
 - Benefits
 - Taxes
 - Caps
 - Brackets
 - Exemptions

Exists only if the implementer defines it through configuration.

## Default Values

The project may offer sensible default values (for example, 30-day months) with the sole purpose of
facilitating initial adoption.

The project declares that:

 - Default values do not represent legal rules.
 - They are completely configurable.
 - They should not be assumed as correct for any specific jurisdiction.

## About Implementer Responsibility

The project declares, openly and honestly, that correct use of the engine requires technical competence.

The implementer is expected to:

 - Have reasonable knowledge of how payroll is calculated.
 - Understand the legal framework applicable to the jurisdiction being configured.
 - Be capable of manually calculating a complete payroll for at least one employee.
 - Compare manual results with system results.
 - Identify configuration errors on their own.

The project does not intend to protect the implementer from errors derived from incorrect configuration.

## Project Philosophy Regarding Errors

The project clearly distinguishes between:

 - Configuration errors, which are the implementer's responsibility.
 - Engine errors, which are the project's responsibility.

When an implementer identifies a possible engine error, it is expected, under a principle of good faith, that:

  - The error be reported.
  - Appropriate context be provided to reproduce the error.

The project may review, analyze, and validate the report.

However:

 - There is no obligation to respond.
 - There is no commitment to correction.
 - There is no guarantee of timelines.

Corrections are made when reasonably possible and when they align with the project's objectives.

It is possible that when implementing the system in a specific jurisdiction, the payroll engine may have technical
limitations that make implementation difficult. These limitations are not considered an error because each jurisdiction or even entity
has different rules for payroll-related calculations. These limitations will be addressed as a request for a new
feature; however, no changes will be implemented in the payroll engine that break the social contract of maintaining a product
completely agnostic to the jurisdiction where it is implemented.

The system commits to providing the foundation for implementing a flexible payroll system with calculations based on configuration rather than
programming.

## License and Software Freedom

The project is distributed under the Apache License, Version 2.0.

In accordance with said license, the project affirms that:

 - The software is provided "as is" (AS IS).
 - No warranties of fitness for a particular purpose are offered.
 - Correct results or legal compliance are not guaranteed.

The project values and promotes:

 - Free use.
 - Modification.
 - Redistribution.
 - Integration into other systems.

Always respecting the terms of the license.

## Role of BMO Soluciones, S.A.

BMO Soluciones, S.A.:

 - Publishes and maintains the project under free software principles.
 - Does not assume responsibility for use of the engine in production.
 - Does not guarantee correct results or legal conformity.
 - Acts as steward of the project, not as a service provider.

## Commitment to Technical Honesty

This project commits to:

 - Not hiding limitations.
 - Not presenting the engine as a system "ready to comply with laws".
 - Not promising more than what the engine can deliver.
 - Maintaining clear documentation about its real scope.

## Final Statement.

This project exists to serve competent implementers who need a flexible and honest payroll calculation engine.
It does not intend to replace professional judgment, legal knowledge, or human responsibility.
The freedom that the engine offers necessarily implies responsibility on the part of whoever uses it.
