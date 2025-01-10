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
import jsonHighlight from '@cloudscape-design/code-view/highlight/json';


export const GeneratorUsage = ({ item, isLoading }) => {
    console.log(item?.iMeta)
    return (
        <Container header={<Header variant="h2">Generator Payload Details</Header>}>
            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <ColumnLayout columns={3} variant="text-grid">
                    <div>
                        <Box variant="awsui-key-label">Generator Model</Box>
                        <div>{item?.p.model_id}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Request ID</Box>
                        <div>{item?.p.req_id}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Parameters</Box>
                        <div>
                            <CodeView content={
                                "{" +
                                "seed: "+item?.p.seed+", "+
                                "temperature: "+(item?.p.temperature || 'undefined')+", "+
                                "top_p: "+(item?.p.top_p || 'undefined')+", "+
                                "no_of_images: "+(item?.p.no_of_images || '') +
                                "}"
                            } />
                        </div>
                    </div>
                </ColumnLayout>
            }
            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <ColumnLayout columns={1} variant="text-grid">
                    <div>
                        <Box variant="awsui-key-label">Payload</Box>
                        <CodeView lineNumbers content={JSON.stringify(item?.p, null, "\t")} />
                    </div>
                </ColumnLayout>
            }

            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <ColumnLayout columns={1} variant="text-grid">
                    <div>
                        <Box variant="awsui-key-label">Generator Response</Box>
                        <CodeView lineNumbers content={JSON.stringify(item?.r, null, "\t")} />
                    </div>
                </ColumnLayout>
            }
        </Container>
    )}