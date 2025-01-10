// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import React, { useState } from 'react';
import {
    Box,
    ColumnLayout,
    Container, Grid,
    Header, Spinner, CopyToClipboard, SpaceBetween, Button, Badge
} from '@cloudscape-design/components';
import { CodeView } from '@cloudscape-design/code-view';

export const GeneratedImage = ({ item, image, isLoading }) => {
    return (
        <Container fitHeight header={<Header variant="h2">Generated Image</Header>}>
            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <img
                    src={image}
                    alt="Generated Image"
                    style={{width: '100%'}}
                    loading="lazy"
                />
            }
        </Container>
    )
}

export const PromptDetails = ({ item, isLoading }) => {
    return (
        <Container header={<Header variant="h2">Prompt Details</Header>}>
            {isLoading ?
                <Spinner size="big" ></Spinner> :
                <ColumnLayout columns={1} variant="text-grid">
                    <div>
                        <Box variant="awsui-key-label">Prompt</Box>
                        <div>
                            <CodeView
                                content={item?.p.prompt}
                            >
                            </CodeView>
                        </div>
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
                    <div>
                        <Box variant="awsui-key-label">Negative Prompts</Box>
                        {item?.p.negative_prompts.map((nP) => (
                            <div>{nP}</div>
                        ))}
                    </div>
                    <Header variant="h2">Inspection Report</Header>
                    <div>
                        <Box variant="awsui-key-label">Inspector</Box>
                        <div>{item?.iMeta.model}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Image Description</Box>
                        <div>{item?.iRes.imageDescription}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Prompt Analysis</Box>
                        <div>{item?.iRes.originalPromptAnalysis}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Policy Voilation</Box>
                        <div>{item?.iRes.policyViolations || "None"}</div>
                    </div>
                    <div>
                        <Box variant="awsui-key-label">Detected Entities</Box>
                        <SpaceBetween
                            direction="horizontal"
                            size="xs"
                        >
                            {
                                item?.iRes?.detectedKeyEntities && item?.iRes?.detectedKeyEntities.length > 0 ?
                                    item?.iRes?.detectedKeyEntities.map(function(value, index){
                                        return <Badge color="blue" key={index}>{value}</Badge>
                                    })
                                    : <div>None</div>
                            }
                        </SpaceBetween>
                    </div>
                    <div>
                        <Container
                            disableContentPaddings
                            disableHeaderPaddings
                            variant="embed"
                            header={
                                <Header
                                    variant="h4"
                                    actions={
                                        <SpaceBetween
                                            direction="horizontal"
                                            size="xs"
                                        >
                                            <Button disabled>Compare with other models</Button>
                                            <CopyToClipboard
                                                copyButtonText="Copy"
                                                copyButtonAriaLabel="Copy Suggested Prompt"
                                                copyErrorText="Suggested Prompt failed to copy"
                                                copySuccessText="Suggested Prompt copied"
                                                textToCopy={item?.iRes.suggestedPrompt|| "None"}
                                            />
                                        </SpaceBetween>
                                    }
                                >
                                    Suggested Prompt
                                </Header>
                            }
                        >
                            <CodeView content={item?.iRes.suggestedPrompt|| "None"}>
                            </CodeView>
                        </Container>
                    </div>
                </ColumnLayout>
            }
        </Container>
    )}

export const ImageAndAnalysis = ({ item, image, isLoading }) => {

    return (
        <Grid
            gridDefinition={[
                { colspan: { l: 6, m: 4, default: 12 } },
                { colspan: { l: 6, m: 8, default: 12 } },
            ]}
        >
            {[
                PromptDetails,
                GeneratedImage,
            ].map((widget, index) => {
                if(index === 0)
                    return <PromptDetails item={item} image={image} />
                else
                    return <GeneratedImage item={item} image={image} />
            })}
        </Grid>
    )}