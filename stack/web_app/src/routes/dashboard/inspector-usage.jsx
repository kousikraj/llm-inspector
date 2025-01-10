// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import React, { useState } from 'react';
import {
    Box,
    ColumnLayout,
    Container,
    Header, Spinner
} from '@cloudscape-design/components';
import { CodeView } from '@cloudscape-design/code-view';


export const InspectorUsage = ({ item, isLoading }) => {
    console.log(item?.iMeta)
    return (
        <Container header={<Header variant="h2">Request Information</Header>}>
            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <ColumnLayout columns={4} variant="text-grid">
                    <div>
                        <Box variant="awsui-key-label">Inspector Model</Box>
                        <div>{item?.iMeta.model}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Request ID</Box>
                        <div>{item?.iMeta.id}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Input Tokens</Box>
                        <div>{item?.iMeta.usage.input_tokens}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Output Tokens</Box>
                        <div>{item?.iMeta.usage.output_tokens}</div>
                    </div>
                </ColumnLayout>
            }
            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <ColumnLayout columns={1} variant="text-grid">
                    <div>
                        <Box variant="awsui-key-label">Response</Box>
                        <CodeView lineNumbers content={JSON.stringify(item?.iRes, null, "\t")} />
                    </div>
                </ColumnLayout>
            }
            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <ColumnLayout columns={1} variant="text-grid">
                    <div>
                        <Box variant="awsui-key-label">Response Meta</Box>
                        <CodeView lineNumbers content={JSON.stringify(item?.iMeta, null, "\t")} />
                    </div>
                </ColumnLayout>
            }
        </Container>
    )}