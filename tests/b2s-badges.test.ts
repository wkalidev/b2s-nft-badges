import { Cl } from "@stacks/transactions";
import { describe, expect, it } from "vitest";

const accounts = simnet.getAccounts();
const owner = accounts.get("wallet_1")!;
const alice = accounts.get("wallet_2")!;
const bob = accounts.get("wallet_3")!;

// Helper function to mint a badge
function mintBadge(recipient: string, badgeId: number, userAmount: number) {
  return simnet.callPublicFn(
    "b2s-badges",
    "mint-badge",
    [Cl.principal(recipient), Cl.uint(badgeId), Cl.uint(userAmount)],
    owner
  );
}

// Helper function to transfer a badge
function transferBadge(tokenId: number, sender: string, recipient: string) {
  return simnet.callPublicFn(
    "b2s-badges",
    "transfer",
    [Cl.uint(tokenId), Cl.principal(sender), Cl.principal(recipient)],
    sender
  );
}

describe("B2S Achievement Badge Tests", () => {
  it("allows owner to mint a badge if user is eligible", () => {
    const { result, events } = mintBadge(alice, 1, 100_000_000);

    expect(result).toBeOk();
    expect(events.length).toBe(1); // nft_mint_event
  });

  it("does not allow minting if user is not eligible", () => {
    const { result } = mintBadge(bob, 2, 500_000_000); // requires 1_000_000_000
    expect(result).toBeErr(Cl.uint(403)); // err-not-eligible
  });

  it("does not allow non-owner to mint", () => {
    const { result } = simnet.callPublicFn(
      "b2s-badges",
      "mint-badge",
      [Cl.principal(bob), Cl.uint(1), Cl.uint(100_000_000)],
      alice
    );
    expect(result).toBeErr(Cl.uint(401)); // err-not-authorized
  });

  it("allows transferring a badge", () => {
    const { result: mintResult } = mintBadge(alice, 1, 100_000_000);
    const tokenId = mintResult.ok; 

    const { result: transferResult } = transferBadge(tokenId, alice, bob);
    expect(transferResult).toBeOk();
  });

  it("does not allow transferring a badge if sender is not owner", () => {
    const { result: mintResult } = mintBadge(alice, 1, 100_000_000);
    const tokenId = mintResult.ok;

    const { result } = transferBadge(tokenId, bob, alice);
    expect(result).toBeErr(Cl.uint(401)); // err-not-authorized
  });

  it("retrieves badge info correctly", () => {
    const { result } = simnet.callReadOnlyFn(
      "b2s-badges",
      "get-badge-info",
      [Cl.uint(1)],
      alice
    );
    expect(result).toBeSome(
      Cl.tuple({
        name: Cl.stringUtf8("Bronze Staker"),
        "badge-type": Cl.stringUtf8("staking"),
        rarity: Cl.stringUtf8("Common"),
        requirement: Cl.uint(100_000_000),
      })
    );
  });

  it("returns last token ID correctly", () => {
    const { result: mintResult1 } = mintBadge(alice, 1, 100_000_000);
    const { result: mintResult2 } = mintBadge(alice, 2, 1_000_000_000);

    const { result } = simnet.callReadOnlyFn(
      "b2s-badges",
      "get-last-token-id",
      [],
      alice
    );
    expect(result).toBeOk(Cl.uint(mintResult2.ok));
  });
});
