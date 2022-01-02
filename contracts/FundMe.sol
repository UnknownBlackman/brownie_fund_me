// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6;

//This import enables us interract with chainlink
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmt;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        //to set a minimum amount that the address can send, in this case 50usd
        //the require keyword is used to set conditions in solidity

        uint256 minUsd = 50 * 10**18;
        require(
            getCoversionUSD(msg.value) >= minUsd,
            "Amount below minimum amount required"
        );

        // msg.sender represents the sender address
        //msg.value represents how much was sent

        addressToAmt[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    //To get real time price of any currency
    //In this case we're getting the price of eth in usd
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        return uint256(answer * 10000000000);
    }

    //To convert the amount funded(which is normally in eth, to USD)

    function getCoversionUSD(uint256 _ethAmount) public view returns (uint256) {
        //1 eth is 1 billion gwei and 1 gwei is 1 billion wei
        uint256 price = getPrice();

        uint256 ethInUSD = (price * _ethAmount) / 1000000000000000000;

        return ethInUSD;
    }

    // Entrance fee
    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        //require(msg.sender == owner); No need for this anymore as the modifier does the job

        //transfer allows us to send eth from one address to another
        //this refers to the address of the contract we're working with
        //so this statement allows us to transfer the entire balance to our address
        payable(msg.sender).transfer(address(this).balance);

        for (
            uint256 fundersIndex = 0;
            fundersIndex < funders.length;
            fundersIndex++
        ) {
            address funder = funders[fundersIndex];
            addressToAmt[funder] = 0;
        }
        funders = new address[](0);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
