// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import React, { useState } from 'react';
import {
  Box,
  ColumnLayout,
  Container,
  Header, Spinner,
  StatusIndicator,
  ContentLayout, SpaceBetween, Tabs
} from '@cloudscape-design/components';
import {PolicyList} from "./policy-list";
import {InspectorUsage} from "./inspector-usage";
import {GeneratorUsage} from "./generator-usage";

export const AuditDetail = ({ item, isLoading }) => {
  const tabs = [
    {
      label: 'Policies',
      id: 'policies',
      content: <PolicyList item={item} isLoading={isLoading} />
    },{
      label: 'Generator Usage',
      id: 'generator-usage',
      content: <GeneratorUsage item={item} isLoading={isLoading} />
    },
    {
      label: 'Inspector Usage',
      id: 'inspector-usage',
      content: <InspectorUsage item={item} isLoading={isLoading} />
    },
  ];
  return (
      <ColumnLayout columns={1} variant="text-grid">
        {/*<Container header={<Header variant="h2">Audit Details</Header>}>*/}
        {/*  */}
        {/*</Container>*/}
        <Tabs tabs={tabs} ariaLabel="Audit details" />
      </ColumnLayout>
)}