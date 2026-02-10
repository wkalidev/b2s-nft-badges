import { Clarinet, Tx, Chain, Account, types } from 'https://deno.land/x/clarinet@v1.0.0/index.ts';
import { assertEquals } from 'https://deno.land/std@0.90.0/testing/asserts.ts';

Clarinet.test({
    name: "Can list a badge for sale",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const seller = accounts.get('wallet_1')!;
        const badgeId = 1;
        const price = 5000000; // 5 tokens
        
        // Set badge owner first
        let setupBlock = chain.mineBlock([
            Tx.contractCall(
                'b2s-marketplace',
                'admin-set-badge-owner',
                [types.uint(badgeId), types.principal(seller.address)],
                seller.address
            )
        ]);
        
        // List badge
        let block = chain.mineBlock([
            Tx.contractCall(
                'b2s-marketplace',
                'list-badge',
                [types.uint(badgeId), types.uint(price)],
                seller.address
            )
        ]);
        
        block.receipts[0].result.expectOk().expectUint(1); // listing-id = 1
        
        // Verify listing
        let getListing = chain.callReadOnlyFn(
            'b2s-marketplace',
            'get-listing',
            [types.uint(1)],
            seller.address
        );
        
        const listing = getListing.result.expectOk().expectSome();
        assertEquals(listing['price'], types.uint(price));
        assertEquals(listing['active'], types.bool(true));
    },
});

Clarinet.test({
    name: "Can cancel a listing",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const seller = accounts.get('wallet_1')!;
        
        // Setup and list
        chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'admin-set-badge-owner',
                [types.uint(1), types.principal(seller.address)],
                seller.address),
            Tx.contractCall('b2s-marketplace', 'list-badge',
                [types.uint(1), types.uint(5000000)],
                seller.address)
        ]);
        
        // Cancel listing
        let cancelBlock = chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'cancel-listing',
                [types.uint(1)],
                seller.address)
        ]);
        
        cancelBlock.receipts[0].result.expectOk().expectBool(true);
        
        // Verify listing is inactive
        let getListing = chain.callReadOnlyFn(
            'b2s-marketplace',
            'get-listing',
            [types.uint(1)],
            seller.address
        );
        
        const listing = getListing.result.expectOk().expectSome();
        assertEquals(listing['active'], types.bool(false));
    },
});

Clarinet.test({
    name: "Can buy a listed badge",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const seller = accounts.get('wallet_1')!;
        const buyer = accounts.get('wallet_2')!;
        const badgeId = 1;
        const price = 5000000;
        
        // Setup, list
        chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'admin-set-badge-owner',
                [types.uint(badgeId), types.principal(seller.address)],
                seller.address),
            Tx.contractCall('b2s-marketplace', 'list-badge',
                [types.uint(badgeId), types.uint(price)],
                seller.address)
        ]);
        
        // Buy badge
        let buyBlock = chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'buy-badge',
                [types.uint(1)],
                buyer.address)
        ]);
        
        buyBlock.receipts[0].result.expectOk().expectUint(1); // sale-id = 1
        
        // Verify ownership transferred
        let getOwner = chain.callReadOnlyFn(
            'b2s-marketplace',
            'get-badge-owner',
            [types.uint(badgeId)],
            buyer.address
        );
        
        getOwner.result.expectOk().expectSome().expectPrincipal(buyer.address);
    },
});

Clarinet.test({
    name: "Cannot buy your own listing",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const seller = accounts.get('wallet_1')!;
        
        // Setup and list
        chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'admin-set-badge-owner',
                [types.uint(1), types.principal(seller.address)],
                seller.address),
            Tx.contractCall('b2s-marketplace', 'list-badge',
                [types.uint(1), types.uint(5000000)],
                seller.address)
        ]);
        
        // Try to buy own listing
        let buyBlock = chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'buy-badge',
                [types.uint(1)],
                seller.address)
        ]);
        
        buyBlock.receipts[0].result.expectErr().expectUint(401); // err-not-authorized
    },
});

Clarinet.test({
    name: "Can update listing price",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const seller = accounts.get('wallet_1')!;
        const oldPrice = 5000000;
        const newPrice = 8000000;
        
        // Setup and list
        chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'admin-set-badge-owner',
                [types.uint(1), types.principal(seller.address)],
                seller.address),
            Tx.contractCall('b2s-marketplace', 'list-badge',
                [types.uint(1), types.uint(oldPrice)],
                seller.address)
        ]);
        
        // Update price
        let updateBlock = chain.mineBlock([
            Tx.contractCall('b2s-marketplace', 'update-price',
                [types.uint(1), types.uint(newPrice)],
                seller.address)
        ]);
        
        updateBlock.receipts[0].result.expectOk().expectBool(true);
        
        // Verify new price
        let getListing = chain.callReadOnlyFn(
            'b2s-marketplace',
            'get-listing',
            [types.uint(1)],
            seller.address
        );
        
        const listing = getListing.result.expectOk().expectSome();
        assertEquals(listing['price'], types.uint(newPrice));
    },
});

Clarinet.test({
    name: "Platform fee calculation is correct",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const wallet = accounts.get('wallet_1')!;
        const price = 10000000; // 10 tokens
        
        // Calculate fee (should be 2.5%)
        let getFee = chain.callReadOnlyFn(
            'b2s-marketplace',
            'calculate-platform-fee',
            [types.uint(price)],
            wallet.address
        );
        
        const fee = getFee.result.expectOk();
        assertEquals(fee, types.uint(250000)); // 0.25 tokens
        
        // Calculate seller amount
        let getSellerAmount = chain.callReadOnlyFn(
            'b2s-marketplace',
            'calculate-seller-amount',
            [types.uint(price)],
            wallet.address
        );
        
        const sellerAmount = getSellerAmount.result.expectOk();
        assertEquals(sellerAmount, types.uint(9750000)); // 9.75 tokens
    },
});