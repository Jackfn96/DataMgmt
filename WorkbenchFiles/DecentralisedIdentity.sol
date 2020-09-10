pragma solidity >=0.4.25 <0.6.0;

contract DecentralisedIdentity
{
    enum StateType { AvailableToShare, SharingRequestPending, SharingWithThirdParty, Terminated }
    address public Owner;
    address public BankAgent;
    string public LockerFriendlyName;
    string public AppUsername;
    address public CurrentAuthorizedUser;
    address public ThirdPartyRequestor;
    string public IntendedPurpose;
    string public LockerStatus;
    string public AppThirdParty;
    StateType public State;

    constructor(string memory lockerFriendlyName, string memory appUsername, address bankAgent) public
    {
        Owner = msg.sender;
        LockerFriendlyName = lockerFriendlyName;
        BankAgent = bankAgent;
        AppUsername = appUsername;
        LockerStatus = "Approved";
        State = StateType.AvailableToShare;
    }

    function ShareWithThirdParty(address thirdPartyRequestor, string memory intendedPurpose,
        string memory appThirdParty) public
    {

        ThirdPartyRequestor = thirdPartyRequestor;
        CurrentAuthorizedUser = ThirdPartyRequestor;
        LockerStatus = "Shared";
        IntendedPurpose = intendedPurpose;
        AppThirdParty = appThirdParty;
        State = StateType.SharingWithThirdParty;
    }

    function AcceptSharingRequest() public
    {

        CurrentAuthorizedUser = ThirdPartyRequestor;
        State = StateType.SharingWithThirdParty;
    }

    function RejectSharingRequest() public
    {
        LockerStatus = "Available";
        CurrentAuthorizedUser = 0x0000000000000000000000000000000000000000;
        State = StateType.AvailableToShare;
        AppThirdParty = "";
    }

    function RequestLockerAccess(string memory intendedPurpose, string memory appThirdParty) public
    {

        ThirdPartyRequestor = msg.sender;
        IntendedPurpose = intendedPurpose;
        State = StateType.SharingRequestPending;
        AppThirdParty = appThirdParty;
    }

    function ReleaseLockerAccess() public
    {

        LockerStatus = "Available";
        ThirdPartyRequestor = 0x0000000000000000000000000000000000000000;
        CurrentAuthorizedUser = 0x0000000000000000000000000000000000000000;
        IntendedPurpose = "";
        State = StateType.AvailableToShare;
        AppThirdParty = "";
    }
    
    function RevokeAccessFromThirdParty() public
    {
        LockerStatus = "Available";
        CurrentAuthorizedUser = 0x0000000000000000000000000000000000000000;
        State = StateType.AvailableToShare;
        AppThirdParty = "";

    }

    function Terminate() public
    {
        CurrentAuthorizedUser = 0x0000000000000000000000000000000000000000;
        State = StateType.Terminated;
    }
}