package se.korkort
import kotlin.test.*
import kotlin.random.Random
class IdentityRejection10KTest {
 @Test fun acceptedStartMustRejectEachInvalidInjectedIdentity() {
  val bank=acceptedPracticeBank9J
  val rows=listOf("missing_content_version" to bank.identity.copy(contentVersion=""),"wrong_content_version" to bank.identity.copy(contentVersion="unrelated-package"),"wrong_manifest_digest" to bank.identity.copy(manifestSha256=Sha256("0".repeat(64)))).map{(name,identity)->
   val error=runCatching{TransientQuizState(countText="1").showSetup().startPractice(bank.copy(identity=identity),Random(1))}.exceptionOrNull()
   mapOf("case" to name,"expected" to "rejected","observed" to if(error is IllegalArgumentException)"rejected" else if(error==null)"accepted" else "unexpected_exception","error" to error?.toString())
  }
  Proof10J.write("10K3","invalid-input-reproduction.json",mapOf("candidate" to acceptedIdentity9J,"cases" to rows,"inherited_defect" to "DEF-10F-001","scope" to "conditional injected bank model; normal App statically uses accepted bank, no package-injection UI/hot replacement"))
  assertTrue(rows.all{it["observed"]=="rejected"},"All invalid bank identities must be rejected; keep inherited expected failure intact")
 }
}
