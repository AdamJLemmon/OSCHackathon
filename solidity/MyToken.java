package com.nuco.api.test;


import com.nuco.api.IContract;
import com.nuco.api.INuco;
import com.nuco.api.impl.Contract;
import com.nuco.api.impl.NucoImpl;
import com.nuco.api.sol.Address;
import com.nuco.api.sol.SolidityAbstractType;
import com.nuco.api.sol.Uint;
import com.nuco.api.types.Types;

import java.util.ArrayList;
import java.util.Map;

public class MyToken {

    public static void main(String[] args) {
        System.out.println("===============  Testing MyToken Contract  ======================");
        INuco api = new NucoImpl();
        api.connect(INuco.LOCALHOST_URL);


        // unlockAccount before deployContract or send a transaction.
        String password = "1";
        byte[] acc = api.getWallet().getAccounts().get(0);
        byte[] acc2 = api.getWallet().getAccounts().get(1);

        if (!api.getWallet().unlockAccount(acc, password, 300)) {
            System.out.println("Unlock account failed!");
            return;
        }

        //String s = "contract MyToken{  event Transfer(address indexed from, address indexed to, uint256 value); string public name;  string public symbol;  uint8 public decimals; mapping(address=>uint256) public balanceOf; function MyToken(uint256 initialSupply, string tokenName, uint8 decimalUnits, string tokenSymbol){ balanceOf[msg.sender]=initialSupply;    name = tokenName;    symbol = tokenSymbol;    decimals = decimalUnits;  } function transfer(address _to,uint64 _value){    if (balanceOf[msg.sender] < _value || balanceOf[_to] + _value < balanceOf[_to]) throw;    balanceOf[msg.sender] -= _value;    balanceOf[_to] += _value;    Transfer(msg.sender, _to, _value); }}";
        String s = "contract MyToken {mapping (address => uint256) public balanceOf;function MyToken(uint256 initialSupply) {balanceOf[msg.sender] = initialSupply;}function transfer(address _to, uint256 _value) {if (balanceOf[msg.sender] < _value) throw;if (balanceOf[_to] + _value < balanceOf[_to]) throw;balanceOf[msg.sender] -= _value;balanceOf[_to] += _value;}}";

        Map<String, Types.CompileResponse> test = api.getTransaction().compile(s);

        ArrayList<SolidityAbstractType> param = new ArrayList<>();
        param.add(Uint.copyFrom(60000));
//            param.add(SString.copyFrom("Nuco coin"));
//            param.add(Uint.copyFrom(10));
//            param.add(SString.copyFrom("NUC"));

        IContract contract = Contract.createFromSource(s, api, 900000L, param);

        //Check initial default account balance
        Types.ContractResponse contractResponse = contract.newFunction("balanceOf")
                .setParam(Address.copyFrom(acc))
                .build()
                .execute();

        for (Object a : contractResponse.data) {
            System.out.println("balanceOf " + api.getUtils().bytes2Hex(acc) + ": " + a.toString());
        }

        //Transfer balance to another account
        contractResponse = contract.newFunction("transfer")
                .setParam(Address.copyFrom(acc2))
                .setParam(Uint.copyFrom(60))
                .build()
                .execute();


        byte[] transHash = contractResponse.TxHash;
        System.out.println("transactionHash: " + api.getUtils().bytes2Hex(transHash));

        Types.TransactionReceipt receipt = new Types.TransactionReceipt();
        int cnt = 300;
        while (receipt.logs == null) {
            receipt = api.getTransaction().getTransactionReceipt(transHash);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e1) {
                e1.printStackTrace();
            }
            if (cnt-- < 0) {
                System.out.println("Missed transaction!");
                api.destroyApi(INuco.LOCALHOST_URL);
            }
        }

        //Check account2's balance
        contractResponse = contract.newFunction("balanceOf")
                .setParam(Address.copyFrom(acc2))
                .build()
                .execute();

        for (Object a : contractResponse.data) {
            System.out.println("new balanceOf " + api.getUtils().bytes2Hex(acc2) + ": " + a.toString());
        }

        //Check account1's balance
        contractResponse = contract.newFunction("balanceOf")
                .setParam(Address.copyFrom(acc))
                .build()
                .execute();

        for (Object a : contractResponse.data) {
            System.out.println("new balanceOf " + api.getUtils().bytes2Hex(acc) + ": " + a.toString());
        }

        api.destroyApi(INuco.LOCALHOST_URL);
    }
}
