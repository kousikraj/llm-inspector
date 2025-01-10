/*
 * # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * # SPDX-License-Identifier: MIT-0
 */

import { createTableSortLabelFn } from "../common/i18n-strings";
import {Popover, Link, StatusIndicator} from "@cloudscape-design/components";
import { SentimentIcon } from "./SentimentIcon";
import { Formatter } from "../format";
import { DateTimeForm, formatDateTime } from './DateTimeForm';
import React from "react";

const rawColumns = [
    {
        id: "mId",
        header: "Model ID",
        cell: e => (
            <Link variant="primary" href={`/dashboard/${e.mId}_${e.rId}`}>
                {e.mId}<br/>
                {e.rId}
            </Link>
        ),
        minWidth: 100,
    }, {
        id: "prompt",
        header: "Prompt",
        cell: e => {
            if (e['p'].prompt !== undefined) {
                return (
                    <Popover
                        dismissButton={false}
                        position="top"
                        size="large"
                        triggerType="text"
                        content={e['p'].prompt}
                    >
                        {(e['p'].prompt.length > 20 ? e['p'].prompt.substring(0, 100) + "..." : e['p'].prompt)}
                    </Popover>
                )
            }
            return 'n/a'
        },
        minWidth: 300,
    }, {
        id: "description",
        header: "Description",
        cell: e => {
            if (e['iRes']?.imageDescription !== undefined) {
                let imageDescription = e['iRes']?.imageDescription
                return (
                    <Popover
                        dismissButton={false}
                        position="top"
                        size="large"
                        triggerType="text"
                        content={imageDescription}
                    >
                        {(imageDescription.length > 20 ? imageDescription.substring(0, 100) + "..." : imageDescription)}
                    </Popover>
                )
            }
        },
        minWidth: 300,
    }, {
        id: "compliant",
        header: "Compliant",
        cell: e => {
            // let policyViolations = e['iRes']?.policyViolations
            let policies =  e['iRes']?.policies
            let noViolations = true
            for (const key in policies) {
                let policy = policies[key]
                if(policy !== "Yes"){
                    noViolations = false;
                    break;
                }
            }
            if(noViolations){
                return <StatusIndicator type="success">Compliant</StatusIndicator>
            }else{
                return <StatusIndicator type="error">Non Compliant</StatusIndicator>
            }
        },
        minWidth: 50,
    }, {
        id: "violation",
        header: "Violation",
        cell: e => {
            if (e['iRes']?.policyViolations !== undefined) {
                let policyViolations = e['iRes']?.policyViolations
                return (
                    <Popover
                        dismissButton={false}
                        position="top"
                        size="large"
                        triggerType="text"
                        content={policyViolations}
                    >
                        {(policyViolations.length > 20 ? policyViolations.substring(0, 100) + "..." : policyViolations)}
                    </Popover>
                )
            }
        },
        minWidth: 300,
    }, {
        id: "suggestedPrompt",
        header: "Suggested Prompt",
        cell: e => {
            if (e['iRes']?.suggestedPrompt !== undefined) {
                let suggestedPrompt = e['iRes']?.suggestedPrompt
                return (
                    <Popover
                        dismissButton={false}
                        position="top"
                        size="large"
                        triggerType="text"
                        content={suggestedPrompt}
                    >
                        {(suggestedPrompt.length > 20 ? suggestedPrompt.substring(0, 100) + "..." : suggestedPrompt)}
                    </Popover>
                )
            }
        },
        minWidth: 300,
    }, {
        id: "date",
        sortingField: "date",
        header: "Time",
        cell: e => (
            <Link variant="primary"
                  href={`/dashboard/${e.mId}_${e.rId}`}>
                {Formatter.Timestamp(Date.parse(e.iTD))}
            </Link>
        ),
        minWidth: 200
    }
];

export const COLUMN_DEFINITIONS = rawColumns.map(column => ({ ...column, ariaLabel: createTableSortLabelFn(column) }));

export const FILTERING_PROPERTIES = [
    {
        key: "mId",
        operators: ["=", "!=", ":", "!:"],
        propertyLabel: "Model ID",
        groupValuesLabel: "Model ID"
    },
    {
        key: "rId",
        operators: ["=", "!=", ":", "!:"],
        propertyLabel: "resource",
        groupValuesLabel: "resource"
    },
    {
        key: "prompt",
        operators: ["=", "!=", ":", "!:"],
        propertyLabel: "Prompt",
        groupValuesLabel: "Prompt"
    },
    {
        key: "conformity",
        operators: ["=", "!=", ":", "!:"],
        propertyLabel: "Conformity",
        groupValuesLabel: "Conformity"
    },
    {
        key: "suggestedPrompt",
        operators: ["=", "!=", ":", "!:"],
        propertyLabel: "Suggested Prompt",
        groupValuesLabel: "Languages Codes"
    },
    {
        key: "date",
        propertyLabel: "DateTime",
        groupValuesLabel: "DateTime",
        defaultOperator: '>',
        operators: ['<', '<=', '>', '>='].map(operator => ({
            operator,
            form: DateTimeForm,
            format: formatDateTime,
            match: 'datetime',
        }))

    }
].sort((a, b) => a.propertyLabel.localeCompare(b.propertyLabel));

export const DEFAULT_PREFERENCES = {
    pageSize: 30,
    wrapLines: false,
    stripedRows: true,
    contentDensity: 'comfortable',
    stickyColumns: { first: 2, last: 0 },
}