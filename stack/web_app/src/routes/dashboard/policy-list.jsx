import * as React from "react";
import Table from "@cloudscape-design/components/table";
import Box from "@cloudscape-design/components/box";
import SpaceBetween from "@cloudscape-design/components/space-between";
import Header from "@cloudscape-design/components/header";
import {Button, StatusIndicator, TextFilter} from "@cloudscape-design/components";
import { useCollection } from '@cloudscape-design/collection-hooks';
import {getTextFilterCounterText} from "../../common/i18n-strings";

export const TableNoMatchState = ({ onClearFilter }) => (
    <Box margin={{ vertical: 'xs' }} textAlign="center" color="inherit">
        <SpaceBetween size="xxs">
            <div>
                <b>No matches</b>
                <Box variant="p" color="inherit">
                    We can't find a match.
                </Box>
            </div>
            <Button onClick={onClearFilter}>Clear filter</Button>
        </SpaceBetween>
    </Box>
);

export const TableEmptyState = ({ resourceName }) => (
    <Box margin={{ vertical: 'xs' }} textAlign="center" color="inherit">
        <SpaceBetween size="xxs">
            <div>
                <b>No {resourceName.toLowerCase()}s</b>
                <Box variant="p" color="inherit">
                    No {resourceName.toLowerCase()}s associated with this resource.
                </Box>
            </div>
            <Button>Create {resourceName.toLowerCase()}</Button>
        </SpaceBetween>
    </Box>
);

export const PolicyList = ({ item, image, isLoading }) => {
    let policies = item?.iRes.policies
    let policyItems = []
    if(policies == null || policies.length === 0){
        policyItems = []
    }
    else{
        let i = 0
        for (const key in policies) {
            let policy = policies[key]
            let icon =<StatusIndicator type="success"></StatusIndicator>
            if (item ===  "Yes") {
                icon = <StatusIndicator type="success"></StatusIndicator>
            }

            policyItems.push({
                index: ++i,
                name: key,
                key: key,
                result: policy
            })
        }
    }
    const { items, actions, filteredItemsCount, collectionProps, filterProps, paginationProps } = useCollection(policyItems, {
        filtering: {
            empty: <TableEmptyState resourceName="Log" />,
            noMatch: <TableNoMatchState onClearFilter={() => actions.setFiltering('')} />,
        },
        pagination: { pageSize: 10 },
    });
    return (
        <Table
            columnDefinitions={[
                {
                    id: "i",
                    header: "No",
                    cell: item => item.index,
                    sortingField: "i"
                },
                {
                    id: "policy",
                    header: "Policy",
                    cell: item => item.name || "-",
                    sortingField: "policy"
                },
                {
                    id: "compliant",
                    header: "Compliant",
                    cell: item => (item.result || "-"),
                    sortingField: "compliant"
                }
            ]}
            enableKeyboardNavigation
            items={items}
            {...collectionProps}
            loadingText="Loading resources"
            sortingDisabled
            stripedRows
            wrapLines
            empty={
                <Box
                    margin={{ vertical: "xs" }}
                    textAlign="center"
                    color="inherit"
                >
                    <SpaceBetween size="m">
                        <b>No policies analyzed</b>
                    </SpaceBetween>
                </Box>
            }
            filter={
                <TextFilter
                    {...filterProps}
                    filteringAriaLabel="Find Policies"
                    filteringPlaceholder="Find Policies"
                    filteringClearAriaLabel="Clear"
                    countText={getTextFilterCounterText(filteredItemsCount)}
                />
            }
            header={<Header> Policy-wise Compliance </Header>}
        />
    );
}