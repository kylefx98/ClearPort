# Translator for JSON-to-Python booleans
false = False
true = True
null = None
# =============================================================================
# CONFIGURATION FILE (config.py)
# =============================================================================
# This file stores all the static settings for the ClearPort application.
# It includes the blockchain network details, the smart contract address, 
# and user-friendly labels to translate blockchain codes into plain English.
# No active code or complex logic belongs in this file.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. APPLICATION DISPLAY SETTINGS
# -----------------------------------------------------------------------------
APP_NAME = "ClearPort"
TAGLINE = "Container Clearance and Risk Management"
DESCRIPTION = "A blockchain-based system for securely tracking, assessing, and clearing shipping containers with role-based control and automated risk handling."
LOGO_PATH = "assets/logo.png" # Place your logo image here

# -----------------------------------------------------------------------------
# 2. BLOCKCHAIN CONNECTION SETTINGS
# -----------------------------------------------------------------------------
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CONTRACT_ADDRESS = "0xb44ae71AE433323a73E41b300857BbDacfb8411A"

# The ABI (Application Binary Interface) tells the application how to talk to the contract.
# Add your full contract ABI below as a placeholder.
CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			},
			{
				"components": [
					{
						"internalType": "bool",
						"name": "highRiskCountryOfOrigin",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "dangerousCargoType",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "historicalSeizureData",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "randomSelection",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "documentationInaccuracy",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "valueMismatch",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "poorImporterHistory",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "suspiciousPackaging",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "irregularFrequency",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "weightMismatch",
						"type": "bool"
					}
				],
				"internalType": "struct ClearPort.RiskFactors",
				"name": "factors",
				"type": "tuple"
			}
		],
		"name": "assessRisk",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"internalType": "enum ClearPort.Role",
				"name": "assignedRole",
				"type": "uint8"
			}
		],
		"name": "assignRole",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "confirmArrival",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "ContainerApproved",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "ContainerCleared",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "importer",
				"type": "address"
			}
		],
		"name": "ContainerCreated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "ContainerFlagged",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "ContainerRejected",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "customsApprove",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "dataHash",
				"type": "string"
			}
		],
		"name": "DataUploaded",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "Delivered",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "InspectionCompleted",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "InspectionStarted",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "markDelivered",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "markInTransit",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "outForDelivery",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "OutForDelivery",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "portAuthorityApprove",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "rejectContainer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "score",
				"type": "uint256"
			}
		],
		"name": "RiskScoreGenerated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "ShipmentArrived",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "ShipmentInTransit",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "containerId",
				"type": "uint256"
			}
		],
		"name": "startInspection",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "shipmentDataHash",
				"type": "string"
			}
		],
		"name": "uploadShipmentData",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "containers",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "importer",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "dataHash",
				"type": "string"
			},
			{
				"internalType": "enum ClearPort.ContainerStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "enum ClearPort.InspectionStatus",
				"name": "inspectionStatus",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "riskScore",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "customsApproved",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "portAuthApproved",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "systemAdmin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "userRoles",
		"outputs": [
			{
				"internalType": "enum ClearPort.Role",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# -----------------------------------------------------------------------------
# 3. HUMAN-READABLE CONSTANTS (Derived from Contract Enums)
# -----------------------------------------------------------------------------
# These dictionaries translate the numeric codes stored on the blockchain 
# into plain-English text for the user interface.

ROLES = {
    0: "No Role Assigned",
    1: "System Administrator",
    2: "Importer",
    3: "Customs Officer",
    4: "Port Authority",
    5: "Logistics Provider",
    6: "Shipping Agent"
}

CONTAINER_STATUS = {
    0: "Record Created",
    1: "Data Uploaded & Secured",
    2: "In Transit (At Sea)",
    3: "Arrived at Destination Port",
    4: "Risk Assessment Completed",
    5: "Flagged for Concern",
    6: "Currently Under Inspection",
    7: "Approved by Authorities",
    8: "Rejected by Authorities",
    9: "Cleared for Release",
    10: "Out for Final Delivery",
    11: "Successfully Delivered"
}

INSPECTION_STATUS = {
    0: "Not Required",
    1: "Pending Inspection",
    2: "Inspection in Progress",
    3: "Completed",
    4: "Approved",
    5: "Rejected"
}