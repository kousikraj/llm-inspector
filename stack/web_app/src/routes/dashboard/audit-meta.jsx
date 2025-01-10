// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import React, { useState } from 'react';
import {
  Box,
  ColumnLayout,
  Container,
  Header, Spinner,
  StatusIndicator,
} from '@cloudscape-design/components';
import {Formatter} from "../../format";

const Compliant = ({item}) => {
  let policies =  item?.iRes?.policies
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
  }else {
    return <StatusIndicator type="error">Non Compliant</StatusIndicator>
  }
};

export const AuditMetaView = ({ item, isLoading }) => {
  return (
  <Container header={<Header variant="h2">Request Information</Header>}>
    {isLoading ?
        <Spinner size="big" ></Spinner> :
        <ColumnLayout columns={4} variant="text-grid">
          <div>
            <Box variant="awsui-key-label">Model ID</Box>
            <div>{item?.mId}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Sequence ID</Box>
            <div>{item?.rId}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Compliant</Box>
            <Compliant item={item}></Compliant>
          </div>
          <div>
            <Box variant="awsui-key-label">Requested at</Box>
            <div>{Formatter.Timestamp(Date.parse(item?.iTD))}</div>
          </div>
        </ColumnLayout>
    }
  </Container>
)}